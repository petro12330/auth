from .tokens import Token
import redis

r = redis.Redis()


def verification_user_token(data: dict) -> dict:
    status = ''
    access_token = data['access_token']
    refresh_access_token = data['refresh_access_token']
    if r.exists(access_token):
        status = 'Success'
    elif r.exists(refresh_access_token):
        status = 'Your access_token was burned'
    return {'status': status}


def crate_user_tokens(access_token_ttl, token_size, refresh_token_tll, user_uuid):
    access_token = Token(token_ttl=access_token_ttl, token_size=token_size)
    r.set(access_token.token, str(user_uuid))
    r.expire(access_token.token, access_token_ttl)
    refresh_token = Token(refresh_token_tll, token_size)
    r.set(refresh_token.token, str(user_uuid))
    r.expire(refresh_token.token, refresh_token_tll)

    return {
        'access_token': access_token.token,
        'access_token_expire': access_token.token_expire,
        'refresh_access_token': refresh_token.token,
        'refresh_access_token_expire': refresh_token.token_expire
    }


def update_user_tokens(data, access_token_ttl, token_size, refresh_token_tll):
    uuid = str(r.get(data))
    r.delete(data)
    return crate_user_tokens(access_token_ttl, token_size, refresh_token_tll, uuid)
