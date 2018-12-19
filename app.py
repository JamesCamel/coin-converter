from bottle import route, run, request, abort, static_file

from fsm import TocMachine
import os



VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
PORT = os.environ['PORT']

machine = TocMachine(
    states=[
        'user',
        'cashSource',
        'cashAmount',
        'cashDest',
        'requestData',
        'pickGraph',
        'showGraph',
        'guide'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'guide',
            'conditions': 'is_going_to_guide'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'cashSource',
            'conditions': 'is_going_to_cashSource'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'state2',
            'conditions': 'is_going_to_state2'
        },
        {
            'trigger': 'advance',
            'source': 'cashSource',
            'dest': 'cashAmount',
            'conditions': 'is_going_to_cashAmount'
        },
        {
            'trigger': 'advance',
            'source': 'cashAmount',
            'dest': 'cashDest',
            'conditions': 'is_going_to_cashDest'
        },
        {
            'trigger': 'advance',
            'source': 'cashDest',
            'dest': 'requestData',
            'conditions': 'is_going_to_requestData'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'pickGraph',
            'conditions': 'is_going_to_pickGraph'
        },
        {
            'trigger': 'advance',
            'source': 'pickGraph',
            'dest': 'showGraph',
            'conditions': 'is_going_to_showGraph'
        },
        {
            'trigger': 'go_back',
            'source': [
                'cashSource',
                'cashAmount',
                'cashDest',
                'requestData',
                'pickGraph',
                'showGraph',
                'guide'
            ],
            'dest': 'user'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)


@route("/webhook", method="GET")
def setup_webhook():
    mode = request.GET.get("hub.mode")
    token = request.GET.get("hub.verify_token")
    challenge = request.GET.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN:
        print("WEBHOOK_VERIFIED")
        return challenge

    else:
        abort(403)


@route("/webhook", method="POST")
def webhook_handler():
    body = request.json
    print('\nFSM STATE: ' + machine.state)
    print('REQUEST BODY: ')
    print(body)

    if body['object'] == "page":
        event = body['entry'][0]['messaging'][0]
        machine.advance(event)
        return 'OK'


@route('/show-fsm', methods=['GET'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return static_file('fsm.png', root='./', mimetype='image/png')


if __name__ == "__main__":
    run(host="0.0.0.0", port=PORT, debug=True, reloader=True)
