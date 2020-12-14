from flask import Flask, redirect, url_for, request, Response
import json
from rover import Rover, InventoryItem
from env import Environment
app = Flask(__name__)
marseEnv = None
myrover = None


@app.route('/api/environment', methods=['PATCH'])
def patchEnvConfig():
    if request.method == 'PATCH':
        mydict = request.get_json()
        global marseEnv
        global myrover

        temperature = mydict.get('temperature', None)
        humidity = mydict.get('humidity', None)
        solar_flare = mydict.get('solar-flare', None)
        storm = mydict.get('storm', None)

        if temperature is not None:
            marseEnv.temperature = temperature
        if humidity is not None:
            marseEnv.humidity = humidity
        if solar_flare is not None:
            marseEnv.solar_flare = solar_flare
            if marseEnv.solar_flare:
                myrover.battery = 11
        if storm is not None:
            marseEnv.storm = storm

        if marseEnv.storm:
            shield_index = None
            for index, item in enumerate(myrover.inventory):
                if item.type == 'storm-shield':
                    shield_index = index
            if shield_index is not None:
                if myrover.inventory[shield_index].qty == 1:
                    myrover.inventory.pop(shield_index)
                else:
                    myrover.inventory[shield_index].qty = myrover.inventory[shield_index].qty - 1
            else:
                func = request.environ.get('werkzeug.server.shutdown')
                if func is None:
                    raise RuntimeError('Not running with the Werkzeug Server')
                func()

        return Response(status=200)


@app.route('/api/environment/configure', methods=['POST'])
def envConfig():
    if request.method == 'POST':
        global marseEnv
        mydict = request.get_json()
        marseEnv = Environment(temperature=mydict.get('temperature'), humidity=mydict.get(
            'humidity'), solar_flare=mydict.get('solar-flare'), storm=mydict.get('storm'), area_map=mydict.get('area-map'))
        if marseEnv.solar_flare:
            myrover.battery = 11

        if marseEnv.storm:
            shield_index = None
            for index, item in enumerate(myrover.inventory):
                if item.type == 'storm-shield':
                    shield_index = index
            if shield_index is not None:
                if myrover.inventory[shield_index].qty == 1:
                    myrover.inventory.pop(shield_index)
                else:
                    myrover.inventory[shield_index].qty = myrover.inventory[shield_index].qty - 1
            else:
                func = request.environ.get('werkzeug.server.shutdown')
                if func is None:
                    raise RuntimeError('Not running with the Werkzeug Server')
                func()

        return Response(status=200)


@app.route('/api/rover/status')
def roverStatus():
    data = json.dumps(
        {
            "rover": myrover.toDict(),
            "environment": marseEnv.toDict()
        }
    )
    return Response(data, status=200)


@app.route('/api/rover/configure', methods=['POST'])
def roverConfig():
    if request.method == 'POST':
        global myrover
        global marseEnv
        mydict = request.get_json()
        location = mydict.get('deploy-point')
        battery = mydict.get('initial-battery')
        inventory = mydict.get('inventory')
        myrover = Rover(location, battery, inventory)

        # set current terrain
        row = location.get('row')
        column = location.get('column')
        marseEnv.terrain = marseEnv.area_map[row, column]
        return Response(status=200)


@app.route('/api/rover/move', methods=['POST'])
def roverMove():
    global myrover
    global marseEnv

    if marseEnv.storm:
        data = {"message": "Cannot move during a storm"}
        return Response(json.dumps(data), status=428)

    if request.method == 'POST':
        mydict = request.get_json()
        direction = mydict.get('direction')

        try:
            row = myrover.location.row
            column = myrover.location.column
            last_row = marseEnv.area_map.shape[0]
            last_column = marseEnv.area_map.shape[1]

            if direction == "up":
                if row > 0:
                    marseEnv.terrain = marseEnv.area_map[row-1, column]
                    myrover.location.row = row - 1
                else:
                    raise Exception
            elif direction == "down":
                if row < last_row:
                    marseEnv.terrain = marseEnv.area_map[row+1, column]
                    myrover.location.row = row + 1
                else:
                    raise Exception
            elif direction == "left":
                if column > 0:
                    marseEnv.terrain = marseEnv.area_map[row, column - 1]
                    myrover.location.column = column - 1
                else:
                    raise Exception
            else:
                if column < last_column:
                    marseEnv.terrain = marseEnv.area_map[row, column + 1]
                    myrover.location.column = column + 1
                else:
                    raise Exception
        except Exception:
            data = {"message": "Can move only within mapped area"}
            return Response(json.dumps(data), status=428)
        else:
            if myrover.battery != 0:
                if myrover.battery < 2:
                    myrover.battery = 11
                else:
                    myrover.battery = myrover.battery - 1

                currentListInventoryItemType = []

                for item in myrover.inventory:
                    if item.type not in currentListInventoryItemType:
                        currentListInventoryItemType.append(item.type)

                if marseEnv.terrain == 'water' and 'water-sample' not in currentListInventoryItemType:
                    singleInventoryItem = InventoryItem(
                        type='water-sample', qty=2, priority=2)
                    myrover.inventory.append(singleInventoryItem)
                elif marseEnv.terrain == 'dirt' and 'rock-sample' not in currentListInventoryItemType:
                    singleInventoryItem = InventoryItem(
                        type='rock-sample', qty=3, priority=3)
                    myrover.inventory.append(singleInventoryItem)

        return Response(status=200)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
