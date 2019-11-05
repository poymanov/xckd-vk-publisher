import requests

API_URL = 'https://api.vk.com/method/{}'
GET_WALL_UPLOAD_SERVER_URL = API_URL.format('photos.getWallUploadServer')
SAVE_ALBUM_URL = API_URL.format('photos.saveWallPhoto')
WALL_POST_URL = API_URL.format('wall.post')


def create_base_request_payload(credentials):
    return {'access_token': credentials['access_token'], 'v': credentials['api_version']}


def create_vk_credentials(access_token, api_version, group_id):
    return {'access_token': access_token, 'api_version': api_version, 'group_id': group_id}


def get_response_content(response):
    if 'error' in response.json():
        raise Exception(response.json()['error']['error_msg'])

    return response.json()['response']


def get_wall_upload_url(credentials):
    payload = create_base_request_payload(credentials)
    payload['group_id'] = credentials['group_id']

    response = requests.get(GET_WALL_UPLOAD_SERVER_URL, payload)
    content = get_response_content(response)

    return content['upload_url']


def upload_image(image_data, upload_url):
    with open(image_data['path'], 'rb') as file:
        response = requests.post(upload_url, files={'photo': file})
        return response.json()


def save_wall_photo(uploaded_image_data, image_caption, credentials):
    payload = create_base_request_payload(credentials)
    payload['group_id'] = credentials['group_id']
    payload['photo'] = uploaded_image_data['photo']
    payload['server'] = uploaded_image_data['server']
    payload['hash'] = uploaded_image_data['hash']
    payload['caption'] = image_caption

    response = requests.post(SAVE_ALBUM_URL, payload)
    content = get_response_content(response)

    return {'id': content[0]['id'], 'owner_id': content[0]['owner_id']}


def publish_to_wall(saved_wall_photo, image_caption, credentials):
    payload = create_base_request_payload(credentials)
    payload['owner_id'] = "-{}".format(credentials['group_id'])
    payload['message'] = image_caption
    payload['from_group'] = 1
    payload['attachments'] = 'photo{}_{}'.format(saved_wall_photo['owner_id'], saved_wall_photo['id'])

    response = requests.post(WALL_POST_URL, payload)
    content = get_response_content(response)

    return content['post_id']
