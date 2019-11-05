import os

from dotenv import load_dotenv

import comics_service
import vk_service

if __name__ == '__main__':
    load_dotenv()

    comics_data = comics_service.get_comics_image_data()
    comics_comment = comics_data['comment']

    vk_credentials = vk_service.create_vk_credentials(os.environ['VK_ACCESS_TOKEN'], os.environ['VK_API_VERSION'],
                                                      os.environ['VK_GROUP_ID'])

    wall_upload_url = vk_service.get_wall_upload_url(vk_credentials)
    uploaded_image_data = vk_service.upload_image(comics_data, wall_upload_url)
    saved_wall_photo = vk_service.save_wall_photo(uploaded_image_data, comics_comment, vk_credentials)
    published_post_id = vk_service.publish_to_wall(saved_wall_photo, comics_comment, vk_credentials)
    comics_service.delete_temp_dir()

    print('Comics published. Id - {}.'.format(published_post_id))
