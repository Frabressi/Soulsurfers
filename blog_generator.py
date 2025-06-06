# blog_generator.py
import os
import glob
import markdown
import frontmatter
from jinja2 import Template
import config  # Importa config per accedere ai template e CSS filename
from bs4 import BeautifulSoup  # Importa BeautifulSoup

# I template Jinja verranno creati quando questa funzione viene chiamata, usando le stringhe da config
post_template_jinja = None
blog_index_template_jinja = None


def generate_blog_pages(current_texts, current_lang_code, blog_config_paths, site_config):
    """
    Genera le pagine del blog.
    blog_config_paths: dizionario con BLOG_POSTS_DIR, BLOG_OUTPUT_DIR_BASE.
    site_config: dizionario con IMAGES_DIR_NAME, CSS_DIR_NAME.
    """
    global post_template_jinja, blog_index_template_jinja
    if post_template_jinja is None:
        post_template_jinja = Template(config.BLOG_POST_TEMPLATE_STR)
    if blog_index_template_jinja is None:
        blog_index_template_jinja = Template(config.BLOG_INDEX_TEMPLATE_STR)

    all_posts_metadata = []
    blog_posts_dir = blog_config_paths['BLOG_POSTS_DIR']
    blog_output_dir_base = blog_config_paths['BLOG_OUTPUT_DIR_BASE']
    images_dir_name = site_config['IMAGES_DIR_NAME']  # Usato per costruire path relativi, anche se non direttamente qui
    css_dir_name = site_config['CSS_DIR_NAME']
    css_common_filename = config.BLOG_COMMON_CSS_FILENAME

    lang_blog_output_dir = os.path.join(blog_output_dir_base, current_lang_code)
    os.makedirs(lang_blog_output_dir, exist_ok=True)

    # --- Funzioni Helper per i Path (definite qui per chiarezza e accesso a current_lang_code) ---
    def get_img_path_from_post_template(img_rel_path_from_root):
        # Usato per l'immagine di copertina nel template del singolo post.
        # Dal post (blog/lang/post.html) all'immagine (images/...)
        # Esempio: img_rel_path_from_root = "images/blog/mio-post/cover.jpg"
        # Risultato: "../../images/blog/mio-post/cover.jpg"
        return f"../../{img_rel_path_from_root}"

    def get_css_path_from_post_template(css_filename_in_css_dir):
        # Dal post (blog/lang/post.html) al CSS (css/...)
        return f"../../{css_dir_name}/{css_filename_in_css_dir}"

    def get_main_site_url_from_post_template():
        # Dal post (blog/lang/post.html) al sito principale (index.html o en/index.html)
        if current_lang_code == 'it':
            return "../../index.html"  # Da blog/it/post.html a index.html
        else:  # 'en'
            return "../../en/index.html"  # Da blog/en/post.html a en/index.html

    def get_img_path_from_index_template(img_rel_path_from_root):
        # Usato per le immagini di anteprima nell'indice del blog.
        # Dall'indice (blog/lang.html) all'immagine (images/...)
        # Esempio: img_rel_path_from_root = "images/blog/mio-post/cover.jpg"
        # Risultato: "../images/blog/mio-post/cover.jpg"
        return f"../{img_rel_path_from_root}"

    def get_css_path_from_index_template(css_filename_in_css_dir):
        # Dall'indice (blog/lang.html) al CSS (css/...)
        return f"../{css_dir_name}/{css_filename_in_css_dir}"

    def get_main_site_url_from_index_template():
        # Dall'indice (blog/lang.html) al sito principale (index.html o en/index.html)
        if current_lang_code == 'it':
            return "../index.html"  # Da blog/it.html a index.html
        else:  # 'en'
            return "../en/index.html"  # Da blog/en.html a en/index.html

    # --- Fine Funzioni Helper ---

    for filepath in glob.glob(os.path.join(blog_posts_dir, "*.md")):
        try:
            post_fm = frontmatter.load(filepath)
        except Exception as e:
            print(f"Errore nel caricare frontmatter da {filepath}: {e}")
            continue

        post_lang = post_fm.get('lang', 'it')
        if post_lang != current_lang_code:
            continue

        # 1. Converti Markdown in HTML grezzo
        raw_html_content = markdown.markdown(post_fm.content, extensions=['fenced_code', 'tables', 'extra', 'sane_lists'])

        # 2. Usa BeautifulSoup per correggere i path delle immagini nel corpo del post
        soup = BeautifulSoup(raw_html_content, 'html.parser')
        for img_tag in soup.find_all('img'):
            original_src = img_tag.get('src')
            if original_src and not original_src.startswith(('http://', 'https://', '/', '../')):
                # Modifica solo i path relativi che non sono già stati aggiustati o esterni/assoluti.
                # Il path nel markdown è relativo alla root del progetto (es. "images/blog/...")
                # La pagina HTML del post sarà in "blog/lang_code/slug.html"
                # Quindi, per arrivare dalla pagina del post alla root e poi a "images/..."
                # servono due "../"
                img_tag['src'] = f"../../{original_src}"

        html_content_corrected = str(soup)  # HTML con path immagini corretti

        filename_no_ext = os.path.splitext(os.path.basename(filepath))[0]
        parts = filename_no_ext.split('-', 3)
        slug_candidate = parts[-1] if len(parts) > 3 and all(p.isdigit() for p in parts[:3]) else filename_no_ext

        slug = post_fm.get('slug', slug_candidate)
        post_url_in_lang_dir = f"{slug}.html"

        post_data_for_template = {
            'title': post_fm.get('title', 'Senza Titolo'),
            'date': post_fm.get('date', 'N.D.'),
            'author': post_fm.get('author', 'Anonimo'),
            'image': post_fm.get('image'),  # Per l'immagine di copertina, gestita da get_image_path nel template
            'content_html': html_content_corrected,  # HTML con path corretti
            'lang': current_lang_code,
            'get_image_path': get_img_path_from_post_template,  # Per l'immagine di copertina
            'blog_index_url': f"../{current_lang_code}.html",
            'get_css_path': get_css_path_from_post_template,
            'css_common_filename': css_common_filename,
            'get_main_site_url': get_main_site_url_from_post_template
        }
        rendered_post_html = post_template_jinja.render(post=post_data_for_template)
        with open(os.path.join(lang_blog_output_dir, post_url_in_lang_dir), "w", encoding="utf-8") as f_post:
            f_post.write(rendered_post_html)

        # Preparazione metadati per la pagina indice del blog
        summary_text = post_fm.get('summary')
        if not summary_text:  # Genera un sommario se non fornito
            # Prendi il primo paragrafo o i primi N caratteri dall'HTML corretto
            summary_soup = BeautifulSoup(html_content_corrected, 'html.parser')
            first_p = summary_soup.find('p')
            if first_p and first_p.get_text():
                summary_text = first_p.get_text(strip=True)[:250] + "..."
            elif html_content_corrected:
                summary_text = html_content_corrected.replace('\n', ' ')[:250].rsplit(' ', 1)[0] + "..."  # Rimuovi tag HTML
                summary_text = BeautifulSoup(summary_text, "html.parser").get_text(strip=True)  # Pulizia finale
            else:
                summary_text = "Leggi di più..."

        all_posts_metadata.append({
            'title': post_fm.get('title', 'Senza Titolo'),
            'date': post_fm.get('date', 'N.D.'),
            'author': post_fm.get('author', 'Anonimo'),
            'url': f"{current_lang_code}/{post_url_in_lang_dir}",
            'image': post_fm.get('image'),  # Path relativo dalla root
            'get_image_path': get_img_path_from_index_template,  # Funzione specifica per l'indice
            'summary': summary_text
        })

    all_posts_metadata.sort(key=lambda p: p.get('date', '1970-01-01'), reverse=True)

    index_data_for_template = {
        'posts': all_posts_metadata,
        'lang_code': current_lang_code,
        'main_site_url': get_main_site_url_from_index_template,
        'get_css_path': get_css_path_from_index_template,
        'css_common_filename': css_common_filename,
    }
    rendered_blog_index_html = blog_index_template_jinja.render(index_data_for_template)
    blog_index_page_path = os.path.join(blog_output_dir_base, f"{current_lang_code}.html")
    with open(blog_index_page_path, "w", encoding="utf-8") as f_index:
        f_index.write(rendered_blog_index_html)

    print(f"Pagine del blog per {current_lang_code.upper()} generate in {lang_blog_output_dir} e indice in {blog_index_page_path}")
    return blog_index_page_path