from instagram import app
from instagram.blueprints.users.model import User

fan_id = 10
idol_id = 20

def test_prep():
    fan = User.query.get(fan_id)
    idol = User.query.get(idol_id)
    print("fan: " + str(fan))
    print("idol: " + str(idol))

    try:
        fan.unfollow(idol)
    except:
        print("not idol")

    try:
        idol.unfollow(fan)
    except:
        print("not idol")

    print("-----> fan fans")
    print(fan.fans)
    print("-----> fan idol")
    print(fan.idols)
    print("-----> idol fans")
    print(idol.fans)
    print("-----> idol idol")
    print(idol.idols)
    print("\n")



@app.cli.command()
def test():
    test_prep()

    fan = User.query.get(fan_id)
    idol = User.query.get(idol_id)

    # Testing
    print("Idol should be in fan's idols list")
    fan.follow(idol)
    print(idol in fan.idols)
    print("-----> Fan's fans")
    print(fan.fans)
    print("-----> Fan's idol")
    print(fan.idols)
    print("-----> Idol's fans")
    print(idol.fans)
    print("-----> Idol's idol")
    print(idol.idols)
    print("\n")

    print("Fans should be in idol's fans list")
    print(fan in idol.fans)
    print("\n")

    print("Should not be able to follow yourself")
    fan.follow(fan)
    print(not fan in fan.idols)
    print("\n")

    print("Should not be able to unfollow someone you haven't followed")
    print(not idol.unfollow(fan))
    print("\n")
