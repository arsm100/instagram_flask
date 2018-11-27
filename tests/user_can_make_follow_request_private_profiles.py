from instagram import app, db
from models.follower_request import FollowerRequest
from models.user import User

fan_id = 2
idol_id = User.query.filter_by(private=True).first().id

def test_prep():
    if not idol_id:
        raise BaseException("No private users")
    FollowerRequest.query.delete()

@app.cli.command('request')
def test_request():
    fan = User.query.get(fan_id)
    idol = User.query.get(idol_id)
    # Testing
    # print("Idol should not be in fan's fans list")
    # test_prep()
    # fan.follow(idol)
    # print(not idol in fan.fans)
    # print("\n")

    # print("fan should not be in idol's fans list")
    # test_prep()
    # fan.follow(idol)
    # print(not fan in idol.fans)
    # print("\n")

    print("Idol should be in fan's follow_requests list")
    test_prep()
    fan.follow(idol)
    print(idol in fan.follow_requests)
    print("\n")

    print("fan should be in idol's follower_requests list")
    test_prep()
    fan.follow(idol)
    print(fan in idol.follower_requests)
    print("\n")
