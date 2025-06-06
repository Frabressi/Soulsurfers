# main.py
import os
from jinja2 import Template
# import shutil # NON PIÙ NECESSARIO PER QUESTO SCOPO SPECIFICO

# Importa da moduli personalizzati
import config
import map_generator
import blog_generator


def get_image_url_for_main_page(filename, lang_code, base_images_dir_name):
    """Calcola il path relativo dell'immagine per la pagina principale (index.html o en/index.html)."""
    if lang_code == 'it':
        return f"{base_images_dir_name}/{filename}"
    else:
        return f"../{base_images_dir_name}/{filename}" 


def build_site():
    os.makedirs(os.path.join(config.BASE_OUTPUT_DIR, "en"), exist_ok=True)

    blog_active = hasattr(config, 'BLOG_POSTS_DIR') and config.BLOG_POSTS_DIR is not None
    if blog_active:
        os.makedirs(os.path.join(config.BASE_OUTPUT_DIR, config.BLOG_OUTPUT_DIR_BASE), exist_ok=True)

        source_css_file_path = os.path.join(config.CSS_DIR_NAME, config.BLOG_COMMON_CSS_FILENAME)
        if not os.path.exists(source_css_file_path):
            print(f"ATTENZIONE: File CSS del blog sorgente '{source_css_file_path}' non trovato.")
            print(f"Crea '{config.CSS_DIR_NAME}/{config.BLOG_COMMON_CSS_FILENAME}' se vuoi uno stile dedicato per il blog.")
            print("I template del blog cercheranno comunque di linkarlo.")

        if not hasattr(config, 'BLOG_POST_TEMPLATE_STR') or not hasattr(config, 'BLOG_INDEX_TEMPLATE_STR'):
            print("ATTENZIONE: I template del blog (BLOG_POST_TEMPLATE_STR, BLOG_INDEX_TEMPLATE_STR) non sono definiti in config.py!")
            print("La generazione del blog potrebbe non funzionare correttamente.")

    html_template_main = Template(config.HTML_TEMPLATE_STR)

    for lang_code in ['it', 'en']:
        current_texts_for_lang = config.TEXT_CONTENT[lang_code].copy()

        map_html_fragment = map_generator.generate_map_for_language(
            lang_code,
            current_texts_for_lang,
            config.MAP_DATA_COORDS
        )

        blog_index_url_relative_to_main = None
        if blog_active:
            blog_config_paths = {
                'BLOG_POSTS_DIR': config.BLOG_POSTS_DIR,
                'BLOG_OUTPUT_DIR_BASE': config.BLOG_OUTPUT_DIR_BASE,
            }
            site_config_for_blog = {
                'IMAGES_DIR_NAME': config.IMAGES_DIR_NAME,
                'CSS_DIR_NAME': config.CSS_DIR_NAME,
            }
            generated_blog_index_path = blog_generator.generate_blog_pages(
                current_texts_for_lang,
                lang_code,
                blog_config_paths,
                site_config_for_blog
            )

            if generated_blog_index_path:
                if lang_code == 'it':
                    blog_index_url_relative_to_main = os.path.join(config.BLOG_OUTPUT_DIR_BASE, f"{lang_code}.html").replace("\\", "/")
                else:
                    blog_index_url_relative_to_main = os.path.join("..", config.BLOG_OUTPUT_DIR_BASE, f"{lang_code}.html").replace("\\", "/")

        render_context = {**current_texts_for_lang}
        render_context['map_html_fragment'] = map_html_fragment
        render_context['blog_index_url'] = blog_index_url_relative_to_main
        render_context['nav_blog'] = current_texts_for_lang.get('nav_blog', 'Blog')

        render_context['gg_photo_url'] = get_image_url_for_main_page(config.GG_PHOTO_FILENAME, lang_code, config.IMAGES_DIR_NAME)
        render_context['paco_photo_url'] = get_image_url_for_main_page(config.PACO_PHOTO_FILENAME, lang_code, config.IMAGES_DIR_NAME)
        render_context['surf_photo_url'] = config.SURF_PHOTO_URL_EXTERNAL
        render_context['bike_setup_photo_url'] = get_image_url_for_main_page(config.BIKE_SETUP_PHOTO_FILENAME, lang_code, config.IMAGES_DIR_NAME)
        render_context['grizl_photo_url'] = get_image_url_for_main_page(config.GRIZL_PHOTO_FILENAME, lang_code, config.IMAGES_DIR_NAME)
        render_context['ocean_crossing_photo_url'] = get_image_url_for_main_page(config.OCEAN_CROSSING_PHOTO_FILENAME, lang_code, config.IMAGES_DIR_NAME)

        if lang_code == 'it':
            render_context['brand_link_url'] = "index.html"
            render_context['it_page_url'] = "index.html"
            render_context['en_page_url'] = "en/index.html"
        else:
            render_context['brand_link_url'] = "../index.html"
            render_context['it_page_url'] = "../index.html"
            render_context['en_page_url'] = "index.html"

        rendered_html_content = html_template_main.render(render_context)

        if lang_code == 'it':
            output_path = os.path.join(config.BASE_OUTPUT_DIR, "index.html")
        else:
            output_path = os.path.join(config.BASE_OUTPUT_DIR, "en", "index.html")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(rendered_html_content)
        print(f"Pagina principale in {lang_code.upper()} salvata in: {output_path}")


if __name__ == "__main__":
    build_site()
    print("\n--- Processo di generazione del sito completato. ---")