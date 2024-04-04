
def get_weather(str):
    return('weather')

def get_app(app):
    return(app)

def getList(dict):
    keys = []
    for key in dict.keys():
        keys.append(key)
    return(keys)

def printApp(appname):
    return(appname)


pairs = { "open iracing" : [get_app, 'iracing'],
          "what is the weather" : [get_weather, '' ],
          "what is your name": "Hello I'm C3PO, human cyborg relations. I am fluent in over six million forms of communication. How can I assist you today?"
        }

entry = 'what is the weather'
response = ''
for i in getList(pairs):
    if i == entry:
        try:
            response = pairs[i][0](pairs[i][1])
        except:
            response = pairs[i]
print(response)