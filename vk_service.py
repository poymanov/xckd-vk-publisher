import requests

API_URL = 'https://api.vk.com/method/{}'
GET_WALL_UPLOAD_SERVER_URL = API_URL.format('photos.getWallUploadServer')
SAVE_ALBUM_URL = API_URL.format('photos.saveWallPhoto')
WALL_POST_URL = API_URL.format('wall.post')


def get_base_request_payload(credentials):
    return {'access_token': credentials['access_token'], 'v': credentials['api_version']}


def create_vk_credentials(access_token, api_version, group_id):
    return {'access_token': access_token, 'api_version': api_version, 'group_id': group_id}


def get_response_content(response):
    if 'error' in response.json():
        raise requests.HTTPError(response.json()['error']['error_msg'])

    return response.json()['response']


def get_wall_upload_url(credentials):
    payload = {
        'group_id': credentials['group_id']
    }

    payload.update(get_base_request_payload(credentials))

    response = requests.get(GET_WALL_UPLOAD_SERVER_URL, payload)
    content = get_response_content(response)

    return content['upload_url']


def upload_image(image_data, upload_url):
    with open(image_data['path'], 'rb') as file:
        response = requests.post(upload_url, files={'photo': file})
        return response.json()


def save_wall_photo(uploaded_image_data, image_caption, credentials):
    payload = {
        'group_id': credentials['group_id'],
        'photo': uploaded_image_data['photo'],
        'server': uploaded_image_data['server'],
        'hash': uploaded_image_data['hash'],
        'caption': image_caption
    }

    payload.update(get_base_request_payload(credentials))

    response = requests.post(SAVE_ALBUM_URL, payload)
    content = get_response_content(response)

    return {'id': content[0]['id'], 'owner_id': content[0]['owner_id']}


def publish_to_wall(saved_wall_photo, image_caption, credentials):
    payload = {
        'owner_id': "-{}".format(credentials['group_id']),
        'message': image_caption,
        'from_group': 1,
        'attachments': 'photo{}_{}'.format(saved_wall_photo['owner_id'], saved_wall_photo['id'])
    }

    payload.update(get_base_request_payload(credentials))

    response = requests.post(WALL_POST_URL, payload)
    content = get_response_content(response)

    return content['post_id']
