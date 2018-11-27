from instagram import app, db
from instagram.blueprints.users.model import User

fan_id = 1
idol_id = 2
idol2_id = 3

def test_prep():
    fan = User.query.get(fan_id)
    idol = User.query.get(idol_id)
    idol2 = User.query.get(idol2_id)

    print(fan)

    try:
        fan.unfollow(idol)
    except:
        print("not idol")

    try:
        fan.unfollow(idol2)
    except:
        print("not idol")

    print("-----> fan's idols")
    print(fan.idols)
    print("\n")



@app.cli.command()
def test():
    test_prep()

    fan = User.query.get(fan_id)
    idol = User.query.get(idol_id)
    idol2 = User.query.get(idol2_id)
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


    print("Idol2 should be in fan's idols list")
    fan.follow(idol2)
    print(idol2 in fan.idols)
    print("\n")

    print("Fan should be in idol2's fans list")
    print(fan in idol2.fans)
    print("\n")

    print(idol.images)
    print(idol2.images)
    print(fan.feed_images)
