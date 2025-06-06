# config.py
import os

# --- 0. HTML Template String (CSS MODIFICATO PER MAPPA) ---
HTML_TEMPLATE_STR = """
<!DOCTYPE html>
<html lang="{{ lang_code }}">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>{{ page_title }}</title>

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;700;800&family=Open+Sans:wght@400;600&display=swap" rel="stylesheet">

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">

    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.css"/>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.css"/>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/gh/marslan390/BeautifyMarker/leaflet-beautify-marker-icon.min.css"/>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet.fullscreen@3.0.0/Control.FullScreen.css"/>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet-minimap/3.6.1/Control.MiniMap.css"/>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet-locatecontrol/0.66.2/L.Control.Locate.min.css"/>

    <style>
        :root {
            --primary-color: #007bff; 
            --secondary-color: #0056b3; 
            --text-dark: #2c3e50;
            --text-light: #555;
            --bg-light: #f4f7f6;
            --bg-white: #ffffff;
            --bg-darker: #eef1f5;
            --navbar-height: 60px; 
            --footer-height: 50px; 
        }

        html { scroll-behavior: smooth; }
        body { 
            font-family: 'Open Sans', sans-serif; 
            background-color: var(--bg-light); 
            color: var(--text-dark); 
            margin: 0; 
            padding-top: var(--navbar-height); 
            line-height: 1.7;
            font-weight: 400;
            padding-bottom: var(--footer-height); 
        }
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Montserrat', sans-serif;
            font-weight: 700;
            color: var(--text-dark);
        }
        .navbar-custom {
            background-color: rgba(255, 255, 255, 0.95);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            height: var(--navbar-height);
            padding: 0.5rem 1rem;
        }
        .navbar-custom .navbar-brand {
            font-family: 'Montserrat', sans-serif;
            font-weight: 800;
            color: var(--primary-color);
            font-size: 1.5rem;
        }
        .navbar-custom .nav-link {
            color: var(--text-light);
            font-weight: 600;
            padding: 0.5rem 1rem;
            transition: color 0.3s ease;
            font-size: 0.95rem;
        }
        .navbar-custom .nav-link:hover,
        .navbar-custom .nav-link.active {
            color: var(--primary-color);
        }
        .navbar-custom .language-switcher a {
            font-size: 1.1rem; 
            padding: 0.3rem 0.7rem; 
            margin-left: 8px;
            text-decoration: none;
            border-radius: 4px;
            color: var(--text-light);
            opacity: 0.7;
        }
        .navbar-custom .language-switcher a:hover {
            opacity: 1;
            color: var(--primary-color);
        }
        .navbar-custom .language-switcher .active-lang {
            opacity: 1;
            font-weight: bold; 
             color: var(--primary-color); 
        }

        .header-banner { 
            background-image: linear-gradient(rgba(0, 0, 0, 0.60), rgba(0, 0, 0, 0.60)), url('{{ surf_photo_url }}');
            background-size: cover;
            background-position: center center;
            color: white; 
            padding: 120px 20px 100px 20px; 
            text-align: center; 
            margin-top: calc(-1 * var(--navbar-height)); 
        }
        .header-banner h1 { 
            font-size: 4rem; 
            font-weight: 800; 
            margin-bottom: 1.2rem; 
            text-shadow: 2px 2px 8px rgba(0,0,0,0.7); 
            color: #fff;
        }
        .header-banner .subtitle { 
            font-family: 'Open Sans', sans-serif;
            font-size: 1.7rem; 
            font-weight: 400; 
            opacity: 0.95; 
            text-shadow: 1px 1px 5px rgba(0,0,0,0.6);
            color: #f0f0f0;
            max-width: 750px;
            margin-left: auto;
            margin-right: auto;
        }
        .content-section { 
            padding: 70px 15px; 
            opacity: 0; 
            transform: translateY(30px); 
            transition: opacity 0.8s ease-out, transform 0.8s ease-out;
        }
        .content-section.visible { opacity: 1; transform: translateY(0); }
        .bg-light-custom { background-color: var(--bg-white); }
        .bg-darker-custom { background-color: var(--bg-darker); }
        .section-title { 
            font-size: 2.8rem; 
            font-weight: 700; 
            color: var(--secondary-color); 
            margin-bottom: 50px; 
            text-align: center; 
            position: relative; 
        }
        .section-title::after { 
            content: ''; display: block; width: 90px; height: 4px; 
            background-color: var(--primary-color); margin: 18px auto 0; border-radius: 2px;
        }
        .character-card { 
            background-color: var(--bg-white); border: none; border-radius: 18px; 
            padding: 40px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.07); 
            text-align: center; 
            transition: transform 0.4s cubic-bezier(0.25, 0.8, 0.25, 1), box-shadow 0.4s cubic-bezier(0.25, 0.8, 0.25, 1); 
            height: 100%; display: flex; flex-direction: column; align-items: center;
        }
        .character-card:hover { transform: translateY(-12px); box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1); }
        .character-card .profile-pic {
            width: 170px; height: 170px; border-radius: 50%;
            object-fit: cover; margin-bottom: 28px;
            border: 6px solid var(--primary-color); box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }
        .character-card h3 { color: var(--text-dark); font-size: 1.7rem; font-weight: 700; margin-bottom: 18px; }
        .character-card p { font-size: 0.98rem; color: var(--text-light); line-height: 1.65; }
        .trip-description p, .equipment-description p { 
            font-size: 1.1rem; text-align: left; margin-bottom: 22px; 
            color: #4a4a4a; max-width: 820px; margin-left: auto; margin-right: auto;
        }
        .trip-description ul { list-style: none; padding-left: 0; max-width: 820px; margin-left: auto; margin-right: auto; }
        .trip-description ul li { 
            padding-left: 2.2em; text-indent: -2.2em; margin-bottom: 15px; 
            font-size: 1.05rem; position: relative;
        }
        .trip-description ul li i.fas { 
            color: var(--primary-color); margin-right: 15px; width: 1.6em; 
            text-align: center; font-size: 1.15em; vertical-align: middle;
        }
        .trip-description ul ul { margin-top: 12px; padding-left: 28px; }
        .equipment-image-container { text-align: center; margin-top: 15px; margin-bottom: 25px; }
        .equipment-image {
            max-width: 80%; 
            height: auto; border-radius: 15px;
            box-shadow: 0 12px 35px rgba(0,0,0,0.1); border: 1px solid #ccc;
        }
        .equipment-image-caption { font-size: 0.92rem; color: #6c757d; margin-top: 18px; font-style: italic; }

        #map-container {
            width: 100%;
            height: clamp(350px, 70vh, 600px); 
            border-radius: 18px;
            overflow: hidden; 
            box-shadow: 0 12px 35px rgba(0,0,0,0.08);
            margin-top: 35px; 
            background-color: #e0e0e0; 
            position: relative; 
            will-change: transform, opacity;
        }
        #map-container .folium-map { 
            width: 100%; 
            height: 100%; 
            position: absolute; 
            top: 0;
            left: 0;
            border-radius: inherit; 
        }
        .leaflet-container {
            background: var(--bg-darker) !important; 
        }

        .leaflet-control-container .leaflet-control-layers {
            opacity: 0.97; border-radius: 10px; box-shadow: 0 3px 12px rgba(0,0,0,0.18);
        }
        .leaflet-control-layers-toggle { width: 42px !important; height: 42px !important; line-height: 42px !important; font-size: 1.25em; }
        .leaflet-control-layers-expanded { padding: 15px; font-size: 1rem; }
        .beautify-marker i.fa { vertical-align: baseline; }
        footer { 
            position: fixed; left: 0; bottom: 0; width: 100%;
            text-align: center; padding: 10px 20px; 
            background-color: var(--text-dark); color: #ced4da; 
            font-size: 0.85rem; z-index: 1000; 
        }
        footer p { margin-bottom: 0; }

        @media (max-width: 991.98px) { 
            :root { --navbar-height: 56px; }
            .header-banner h1 { font-size: 3.2rem; } 
            .header-banner .subtitle { font-size: 1.5rem; } 
            .section-title { font-size: 2.5rem; }
            .character-card { padding: 30px; }
            .character-card .profile-pic { width: 150px; height: 150px; }
            .navbar-custom .navbar-brand { font-size: 1.3rem; }
            .navbar-custom .nav-link { font-size: 0.9rem; padding: 0.5rem 0.8rem;}
            .navbar-custom .language-switcher { display: flex; align-items: center; }
            .navbar-custom .navbar-collapse.show, 
            .navbar-custom .navbar-collapse.collapsing {
                background-color: var(--bg-white); 
                box-shadow: 0 8px 16px rgba(0,0,0,0.15); 
                border-bottom-left-radius: .5rem;
                border-bottom-right-radius: .5rem;
                padding: 1rem; 
                margin-top: 0; 
                border-top: 1px solid var(--bg-darker); 
            }
            .navbar-custom .navbar-collapse .nav-item { margin-bottom: 0.5rem; }
            .navbar-custom .navbar-collapse .nav-link { color: var(--text-dark) !important; padding: .5rem 0; }
            .navbar-custom .navbar-collapse .nav-link:hover,
            .navbar-custom .navbar-collapse .nav-link.active { color: var(--primary-color) !important; }
            .navbar-custom .navbar-collapse .language- switcher { justify-content: flex-start; padding: .5rem 0; }
        }

        @media (max-width: 768px) { 
            .header-banner { padding: 100px 15px 80px 15px; }
            .header-banner h1 { font-size: 2.6rem; } 
            .header-banner .subtitle { font-size: 1.3rem; } 
            .section-title { font-size: 2.1rem; }
            .content-section { padding: 50px 15px; }
            .character-card { margin-bottom: 30px; } 
            .character-card .profile-pic { width: 130px; height: 130px; }
            .trip-description p, .equipment-description p { font-size: 1.05rem; }
            .equipment-image { max-width: 90%; }
            #map-container { 
                height: clamp(300px, 55vh, 450px);
            } 
            .navbar-toggler { margin-right: 0.5rem;}
            footer { font-size: 0.8rem; padding: 8px 15px;} 
            :root { --footer-height: 40px; }
        }
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-custom fixed-top">
        <div class="container">
            <a class="navbar-brand" href="{{ brand_link_url }}">SaltRiders</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link active" href="#home">{{ nav_home }}</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#mappa">{{ nav_map }}</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#protagonisti">{{ nav_protagonists }}</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#avventura">{{ nav_adventure }}</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#attrezzatura">{{ nav_equipment }}</a>
                    </li>
                    {% if blog_index_url %}
                    <li class="nav-item">
                        <a class="nav-link" href="{{ blog_index_url }}">{{ nav_blog }}</a>
                    </li>
                    {% endif %}
                </ul>
                <div class="language-switcher d-flex align-items-center">
                    <a href="{{ it_page_url }}" class="{{ 'active-lang' if lang_code == 'it' else '' }}" title="Italiano">🇮🇹</a>
                    <a href="{{ en_page_url }}" class="{{ 'active-lang' if lang_code == 'en' else '' }}" title="English">🇬🇧</a>
                </div>
            </div>
        </div>
    </nav>

    <header class="header-banner" id="home">
        <div class="container">
            <h1>{{ header_title }}</h1>
            <p class="subtitle">{{ header_subtitle }}</p>
        </div>
    </header>

    <section id="mappa" class="content-section bg-light-custom">
        <div class="container">
            <h2 class="section-title">{{ map_section_title }}</h2>
            <div id="map-container">
                {{ map_html_fragment | safe }}
            </div>
        </div>
    </section>

    <section id="protagonisti" class="content-section">
        <div class="container">
            <h2 class="section-title">{{ protagonists_section_title }}</h2>
            <div class="row justify-content-center">
                <div class="col-lg-5 col-md-6 mb-4 mb-lg-0">
                    <div class="character-card">
                        <img src="{{ gg_photo_url }}" alt="{{ gg_alt_text }}" class="profile-pic">
                        <h3>{{ gg_name }}</h3>
                        <p>{{ gg_description }}</p>
                    </div>
                </div>
                <div class="col-lg-5 col-md-6">
                    <div class="character-card">
                        <img src="{{ paco_photo_url }}" alt="{{ paco_alt_text }}" class="profile-pic">
                        <h3>{{ paco_name }}</h3>
                        <p>{{ paco_description }}</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <section id="avventura" class="content-section bg-light-custom">
        <div class="container trip-description">
            <h2 class="section-title">{{ adventure_section_title }}</h2>
            <div class="equipment-image-container" style="margin-bottom: 40px;"> 
                <img src="{{ ocean_crossing_photo_url }}" alt="{{ ocean_crossing_alt }}" class="equipment-image" style="max-width: 85%; border: 2px solid var(--primary-color);">
                 <p class="equipment-image-caption"><em>{{ ocean_crossing_caption }}</em></p>
            </div>
            <p class="text-center">{{ adventure_intro1 }}</p>
            <p class="text-center">{{ adventure_intro2 }}</p>
            <ul>
                <li><i class="fas fa-train-subway"></i> <strong>{{ adventure_step1_title }}:</strong> {{ adventure_step1_desc }}</li>
                <li><i class="fas fa-person-biking"></i> <strong>{{ adventure_step2_title }}:</strong> {{ adventure_step2_desc }}</li>
                <li><i class="fas fa-person-biking"></i> <strong>{{ adventure_step3_title }}:</strong> {{ adventure_step3_desc }}</li>
                <li><i class="fas fa-sailboat"></i> <strong>{{ adventure_step4_title }}:</strong> {{ adventure_step4_desc }}</li>
                <li><i class="fas fa-route"></i> <strong>{{ adventure_step5_title }}:</strong>
                    <ul style="margin-top: 10px; padding-left: 25px;">
                        <li><i class="fas fa-ship"></i> <em>{{ adventure_step5_optionA_title }}:</em> {{ adventure_step5_optionA_desc }}</li>
                        <li><i class="fas fa-bicycle"></i> <em>{{ adventure_step5_optionB_title }}:</em> {{ adventure_step5_optionB_desc }}</li>
                    </ul>
                </li>
            </ul>
            <p class="text-center mt-4">{{ adventure_outro }}</p>
        </div>
    </section>

    <section id="attrezzatura" class="content-section bg-darker-custom">
        <div class="container equipment-description">
            <h2 class="section-title">{{ equipment_section_title }}</h2>
            <p class="text-center">{{ equipment_desc1 }}</p>
            <div class="equipment-image-container">
                <img src="{{ bike_setup_photo_url }}" alt="{{ equipment_image_alt }}" class="equipment-image">
                 <p class="equipment-image-caption"><em>{{ equipment_image_caption }}</em></p>
            </div>
            <p class="text-center">{{ equipment_desc2 }}</p> 
            <div class="equipment-image-container">
                <img src="{{ grizl_photo_url }}" alt="{{ grizl_image_alt }}" class="equipment-image">
                 <p class="equipment-image-caption"><em>{{ grizl_image_caption }}</em></p>
            </div>
        </div>
    </section>

    <footer>
        <div class="container">
            <p>{{ footer_text }}</p>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/leaflet@1.9.3/dist/leaflet.js"></script>
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script> 

    <script src="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js"></script>
    <script src="https://cdn.jsdelivr.net/gh/marslan390/BeautifyMarker/leaflet-beautify-marker-icon.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/leaflet.fullscreen@3.0.0/Control.FullScreen.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet-minimap/3.6.1/Control.MiniMap.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet-locatecontrol/0.66.2/L.Control.Locate.min.js"></script>

    <script>
        function onDocumentReady(fn) {
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', fn);
            } else {
                fn(); 
            }
        }
        function onWindowLoad(fn) {
            if (document.readyState === 'complete') {
                fn(); 
            } else {
                window.addEventListener('load', fn);
            }
        }
        var leafletMapInstances = []; 
        function invalidateAllMapsSize() {
            leafletMapInstances.forEach(function(mapInstance) {
                if (mapInstance && typeof mapInstance.invalidateSize === 'function') {
                    mapInstance.invalidateSize({ animate: false });
                }
            });
        }
        function initializeMapLogic() {
            if (typeof L !== 'undefined') {
                var mapDivs = document.querySelectorAll('#map-container .folium-map');
                mapDivs.forEach(function(div) {
                    if (div._leaflet_map && leafletMapInstances.indexOf(div._leaflet_map) === -1) {
                        leafletMapInstances.push(div._leaflet_map);
                    }
                });
                invalidateAllMapsSize();
            }
        }
        onDocumentReady(function () {
            initializeMapLogic();
            const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
            navLinks.forEach(link => {
                link.addEventListener('click', function (e) {
                    const href = this.getAttribute('href');
                    if (href && href.startsWith('#')) {
                        e.preventDefault();
                        const targetId = href.substring(1);
                        const targetElement = document.getElementById(targetId);
                        if (targetElement) {
                            const navbarHeight = document.querySelector('.navbar-custom').offsetHeight;
                            let headerOffset = navbarHeight;
                            if (targetId === 'home') {
                                window.scrollTo({ top: 0, behavior: 'smooth' });
                            } else {
                                const elementPosition = targetElement.getBoundingClientRect().top;
                                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                                window.scrollTo({ top: offsetPosition, behavior: 'smooth' });
                            }
                            const navbarToggler = document.querySelector('.navbar-toggler');
                            const navbarCollapse = document.querySelector('.navbar-collapse');
                            if (navbarToggler && navbarCollapse.classList.contains('show')) {
                                navbarToggler.click(); 
                            }
                        }
                    }
                });
            });
            const sections = document.querySelectorAll('.header-banner, .content-section');
            const observerOptions = {
                root: null,
                rootMargin: "0px 0px -40% 0px", 
                threshold: 0.05 
            };
             const sectionObserver = new IntersectionObserver((entries, observer) => {
                let intersectingEntry = null;
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        if (!intersectingEntry || entry.boundingClientRect.top < intersectingEntry.boundingClientRect.top || entry.intersectionRatio > intersectingEntry.intersectionRatio) {
                            intersectingEntry = entry;
                        }
                    }
                    if (entry.isIntersecting && (entry.target.classList.contains('content-section') || entry.target.classList.contains('header-banner'))) {
                        entry.target.classList.add('visible');
                    }
                });
                if (intersectingEntry) {
                    const id = intersectingEntry.target.getAttribute('id');
                    if (id) {
                        const navLink = document.querySelector(`.navbar-nav .nav-link[href="#${id}"]`);
                        if (navLink) {
                            document.querySelectorAll('.navbar-nav .nav-link').forEach(link => link.classList.remove('active'));
                            navLink.classList.add('active');
                        }
                    }
                }
            }, observerOptions);
            sections.forEach(section => { sectionObserver.observe(section); });
            function setActiveLinkOnLoad() {
                let firstVisibleSectionId = 'home'; 
                let maxVisibility = 0;
                const navbarHeight = document.querySelector('.navbar-custom')?.offsetHeight || 60;
                for (const section of sections) {
                    const rect = section.getBoundingClientRect();
                    const visibleHeight = Math.max(0, Math.min(rect.bottom, window.innerHeight) - Math.max(rect.top, navbarHeight));
                    if (rect.top < window.innerHeight - navbarHeight && rect.bottom > navbarHeight) { 
                        if (section.id === 'home' && rect.top <= navbarHeight + 5) { 
                            firstVisibleSectionId = 'home';
                            maxVisibility = Infinity; 
                            break; 
                        }
                        if (maxVisibility !== Infinity) { 
                            if (rect.top < (document.getElementById(firstVisibleSectionId)?.getBoundingClientRect().top || Infinity) ) {
                                firstVisibleSectionId = section.id;
                            }
                        }
                    }
                    if (section.id === firstVisibleSectionId && !section.classList.contains('visible')) {
                         section.classList.add('visible');
                    }
                }
                document.querySelectorAll('.navbar-nav .nav-link').forEach(link => link.classList.remove('active'));
                const activeNavLink = document.querySelector(`.navbar-nav .nav-link[href="#${firstVisibleSectionId}"]`);
                if (activeNavLink) {
                    activeNavLink.classList.add('active');
                }
            }
            setTimeout(setActiveLinkOnLoad, 150); 
        });
        onWindowLoad(function() {
            setTimeout(invalidateAllMapsSize, 100); 
            var resizeDebounceTimeout;
            window.addEventListener('resize', function() {
                clearTimeout(resizeDebounceTimeout);
                resizeDebounceTimeout = setTimeout(function() {
                    invalidateAllMapsSize();
                }, 250); 
            });
            document.addEventListener('visibilitychange', function() {
                if (document.visibilityState === 'visible') {
                    setTimeout(function() {
                        invalidateAllMapsSize();
                    }, 200); 
                }
            });
        });
    </script>
</body>
</html>
"""

# --- Testi ---
# config.py

# ... (il resto del file, come HTML_TEMPLATE_STR, rimane invariato sopra questo blocco) ...

# --- Testi ---
TEXT_CONTENT = {
    'it': {
        'lang_code': 'it',
        'page_title': "SaltRiders: L'Avventura Epica (e un po' Folle) di GG & Paco - Itinerario 2025-2026",
        'nav_home': "Home",
        'nav_protagonists': "Eroi (o Anti-Eroi?)",
        'nav_adventure': "L'Odissea",
        'nav_equipment': "Ferraglia & Sogni",
        'nav_map': "La Mappa del Viaggio",
        'nav_blog': "Diario di Bordo", # AGGIUNTO PER IL BLOG
        'header_title': "SaltRiders World Tour",
        'header_subtitle': "L'incredibile itinerario 2025-2026 di GG & Paco, un'epopea via terra e mare all'insegna del bikepacking, del surf, dello slow travel e di un approccio sostenibile all'esplorazione.", # MODIFICATO
        'protagonists_section_title': "I Nostri Eroi (Più o Meno)",
        'gg_alt_text': "Foto di GG pronto per l'avventura",
        'gg_name': "GG - Il Gigante Entusiasta",
        'gg_description': "Spirito libero con una riserva inesauribile di entusiasmo (e forse un pizzico di sana incoscienza). GG affronta ogni sfida, anche la più assurda, con un entusiasmo che potrebbe svegliare un vulcano spento. La sua missione: trasformare ogni giorno in un'avventura memorabile, collezionando amici e aneddoti improbabili.",
        'paco_alt_text': "Foto di Paco, perso per le montagne",
        'paco_name': "Paco - L'Esploratore Sagace",
        'paco_description': "Mente acuta e animo energico, Paco è l'anima organizzatrice del duo. Sempre pronto a trovare soluzioni geniali (o almeno, che sembrano tali al momento), affronta ogni peripezia con una buona dose di problem solving creativo. L’adrenalina della scoperta lo guida, trasformando ogni imprevisto in… beh, in un altro imprevisto da risolvere.",
        'adventure_section_title': "La Nostra Gloriosa Odissea",
        'ocean_crossing_alt': "Barca a vela in navigazione oceanica sotto un cielo blu",
        'ocean_crossing_caption': "L'immensità dell'oceano ci attende: la prossima grande sfida.",
        'adventure_intro1': "Allacciate le cinture! Noi SaltRiders, GG e Paco, stiamo per intraprendere un'odissea che riscriverà le regole dell'esplorazione... o almeno, ci proveremo con stile. Dal cuore pulsante dell'Europa, questi due intrepidi avventurieri scateneranno le loro fidate bici e tavole da surf in un tour de force via terra e mare, pronti a collezionare culture esotiche e panorami da cartolina, il tutto con un occhio di riguardo per l'ambiente e le comunità locali.", # MODIFICATO
        'adventure_intro2': "La nostra filosofia di viaggio? Più che un piano, è un manifesto allo **slow travel** e alla **sostenibilità**. Una dichiarazione d'intenti che abbraccia l'imprevisto, l'ingegno e la profonda connessione con i luoghi e le persone, privilegiando la forza delle nostre gambe e mezzi a basso impatto per muoverci nel mondo, evitando il più possibile gli aerei.", # MODIFICATO
        'adventure_step1_title': "Europa Express, con la Calma dei Campioni",
        'adventure_step1_desc': "Da Milano, un inizio 'soft' su rotaia verso ovest, assaporando il Vecchio Continente a un ritmo che ci permette di connetterci veramente con i paesaggi, prima del vero caos.", # MODIFICATO
        'adventure_step2_title': "Scalate Epiche (e Forse Poco Sensate)",
        'adventure_step2_desc': "Un avvio in bicicletta da Torino, con l'ardua impresa di valicare un importante passo alpino con tavole al seguito, per planare (si spera con tutte le ossa intere) su Grenoble. Chi sano di mente lo farebbe? Noi! Seguirà un trasferimento via terra più convenzionale verso San Sebastián, dove l'asfalto tornerà a chiamare le nostre ruote.", # MODIFICATO
        'adventure_step3_title': "Cavalcando l'Atlantico Iberico (e le Salite)",
        'adventure_step3_desc': "Pedalando come se non ci fosse un domani da San Sebastián lungo le coste selvagge di Spagna e Portogallo, alla ricerca di spot da urlo, onde perfette e, possibilmente, un posto dove montare la tenda.",
        'adventure_step4_title': "Rotta per i Caraibi",
        'adventure_step4_desc': "Da Las Palmas de Gran Canaria, ci intrufoleremo nella flotta dell'ARC (Atlantic Rally for Cruisers) il 23 Novembre 2025. L'obiettivo: trovare un imbarco direttamente sui pontili o tramite contatti improbabili. Pronti ad attraversare l'Atlantico veleggiando verso Saint Lucia, sperando di non finire a lavare i piatti per tutta la traversata.",
        'adventure_step5_title': "Sogno Pacifico: Due Destini, Stessa Follia",
        'adventure_step5_optionA_title': "Opzione A - Traversata Oceanica da veri Lupi di Mare (o quasi)",
        'adventure_step5_optionA_desc': "Dai Caraibi, un passaggio 'al volo' via mare per Panama. Da lì, l'immensità del Pacifico: un'avventura di pura navigazione verso perle come le Galápagos e le isole della Polinesia Francese, affidandoci al buon cuore delle onde, dei venti e di chiunque abbia una cuccetta libera.",
        'adventure_step5_optionB_title': "Opzione B - Radici Sudamericane e Polpacci d'Acciaio",
        'adventure_step5_optionB_desc': "Un passaggio marittimo dai Caraibi all'Ecuador segnerà l'inizio di una LUNGA pedalata. Giù per la costa Pacifica del Sudamerica, inseguendo onde mitiche, attraversando deserti e montagne che metteranno alla prova anche i più stoici. Un'immersione nel cuore pulsante del continente fino al Cile, o finché le nostre gambe reggeranno.", # MODIFICATO
        'adventure_outro': "Dimenticate le tabelle di marcia precise: questo è più un manifesto al viaggio vissuto con spirito indomito e consapevolezza, un brindisi all'imprevisto che diventa la norma, a un'esplorazione che rispetta i ritmi della natura e delle culture, e un tributo a ogni singola, strampalata, meravigliosa connessione umana. Restate sintonizzati, perché il bello deve ancora venire (e probabilmente non andrà come previsto)!", # MODIFICATO
        'equipment_section_title': "L'Arsenale dei Sognatori: Bici, Surf & Tenda",
        'equipment_desc1': "L'essenza di un'avventura così particolare risiede anche nella genialità della semplicità e in un pizzico di spirito d’adattamento. Per affrontare le lunghe tratte costiere, noi SaltRiders abbiamo scelto bici gravel equipaggiate con supporti laterali dedicati per trasportare le nostre amate tavole da surf. Questo sistema ingegnoso ci permette di essere agili come gazzelle (carichi come muli) e vivere appieno l’esperienza del viaggio a misura d’uomo e di tavola.", # MODIFICATO
        'equipment_desc2': "Il supporto è leggero ma resistente, e se il vento laterale si farà sentire… fa parte dell’avventura. Con noi anche una tenda compatta, per fermarci dove capita e dormire sotto le stelle, pronti a ripartire all’alba con la fedele compagna d’onda sempre al nostro fianco, come un’appendice aerodinamica un po’ sbilenca ma indispensabile.", # MODIFICATO
        'equipment_image_alt': "Bikepacking con tavola da surf: l'essenza SaltRiders!",
        'equipment_image_caption': "Il nostro assetto da SaltRiders: bici, tavola e orizzonti infiniti.",
        'grizl_image_alt': "Bici gravel Grizl pronta per l'avventura su sterrato",
        'grizl_image_caption': "La nostra fidata compagna a due ruote, pronta ad affrontare ogni tipo di terreno.",
        'map_section_title': "La Mappa del Viaggio",
        'footer_text': "© 2024 SaltRiders Adventures - GG & Paco. Mappa generata con Folium (e tanta pazienza). Stay Stoked!",
        'map_tile_clear': "Mappa Chiara",
        'map_tile_standard': "Mappa Standard",
        'map_tile_satellite': "Mappa Satellitare",
        'map_main_group': "Percorso Principale (Teorico)",
        'map_planA_group': "Opzione Pacifico: Traversata Oceanica",
        'map_planB_group': "Opzione Pacifico: Bici Sudamerica",
        'map_milan_popup': "Milano - Qui inizia la follia!", 'map_milan_date': "10 Set 25",
        'map_turin_popup': "Torino - Pronti per le Alpi?!", 'map_turin_date': "10 Set 25",
        'map_train_tooltip': "Treno Milano→Torino (10 Set 25) - Il riscaldamento",
        'map_turin_bike_popup': "Torino - Inizio Bici (e sofferenza alpina)",
        'map_grenoble_popup': "Grenoble - Sopravvissuti alle Alpi!", 'map_grenoble_date': "11 Set 25",
        'map_bike1_tooltip': "Bici Torino→Grenoble (10-11 Set 25) - 'Una passeggiata', dicevano...",
        'map_grenoble_bus_popup': "Grenoble - Pausa tattica in bus", 'map_grenoble_bus_date': "11 Set 25",
        'map_sanseb_bus_popup': "San Sebastián - Rieccoci!", 'map_sanseb_bus_date': "12 Set 25",
        'map_bus_tooltip': "Bus Grenoble→San Sebastián (11-12 Set 25) - Civilizzazione temporanea",
        'map_sanseb_bike_popup': "San Sebastián - Si riparte a pedalare sulla costa!",
        'map_iberia_bike_tooltip': "Bici Costa Atlantica (14 Set - 28 Ott 25) - Gambe, onde e tapas",
        'map_faro_sail_popup': "Faro - Cercasi passaggio per l'Atlantico", 'map_faro_sail_date': "29 Ott 25",
        'map_las_palmas_popup': "Las Palmas, Gran Canaria - Pronti per l'ARC (o quasi)", 'map_las_palmas_date': "23 Nov 25",
        'map_sail_canaries_tooltip': "Vela Faro→Las Palmas (29 Ott - 03 Nov 25) - Allenamento Atlantico",
        'map_canaries_stop_tooltip': "Sosta e preparativi (panico?) ARC a Gran Canaria\n03 Nov - 23 Nov 25",
        'map_st_lucia_popup': "Saint Lucia, Caraibi - Terra! (Finalmente)", 'map_st_lucia_date': "10-15 Dic 25",
        'map_arc_tooltip': "ARC: Traversata Atlantica (23 Nov - 10/15 Dic 25) - Onde, stelle e mal di mare",
        'map_caribbean_explore_tooltip': "Esplorazione Caraibi (e recupero energie)\n15 Dic 25 - 15 Feb 26",
        'map_panama_transfer_popup': "Panama City - Verso il Grande Blu (Pacifico)", 'map_panama_transfer_date': "16 Feb 26",
        'map_sea_transfer_panama_tooltip': "Passaggio via mare Caraibi→Panama (Feb 26) - Si cambia oceano!",
        'map_panama_prep_tooltip': "Preparativi a Panama (e ricerca mappe del tesoro)\n16 Feb - 28 Feb 26",
        'map_panama_pacific_start_popup': "Panama - Inizio Traversata Pacifico (all'arrembaggio!)", 'map_panama_pacific_start_date': "01 Mar 26",
        'map_sail_leg_tooltip_prefix': "Vela",
        'map_stopover_tooltip_prefix': "Sosta a",
        'map_ecuador_transfer_popup': "Guayaquil, Ecuador - Inizio Avventura Sudamericana",
        'map_ecuador_transfer_date': "16 Feb 26",
        'map_sea_transfer_ecuador_tooltip': "Passaggio via mare Caraibi→Ecuador (Feb 26) - Rotta a Sud!",
        'map_ecuador_explore_tooltip': "Esplorazione Ecuador (e acclimatamento)\n16 Feb - 01 Mar 26",
        'map_guayaquil_bike_popup': "Guayaquil - Inizio Bike Pacifica (e che il dio del ciclismo ci assista)",
        'map_bike_pacific_tooltip': "Bike Costa Pacifica (Mar - Lug 26) - Chilometri, sudore e panorami",
        'map_finisterre_name': "Finisterre", 'map_porto_name': "Porto", 'map_ericeira_name': "Ericeira", 'map_lisbon_name': "Lisbona", 'map_sagres_name': "Sagres", 'map_faro_name': "Faro",
        'map_galapagos_name': "Galápagos", 'map_marquesas_name': "Marchesi", 'map_tahiti_name': "Tahiti",
        'map_montanita_name': "Montañita", 'map_lobitos_name': "Lobitos", 'map_lima_name': "Lima", 'map_iquique_name': "Iquique", 'map_pichilemu_name': "Pichilemu",
        'map_fullscreen_title': "Schermo Intero (Modalità Cinema)",
        'map_fullscreen_cancel': "Esci da Schermo Intero (Ritorno alla Realtà)",
        'map_locate_title': "Dove Diavolo Sono?",
        'map_locate_popup': "Sei qui (più o meno... speriamo)",
    },
    'en': {
        'lang_code': 'en',
        'page_title': "SaltRiders: GG & Paco's Epic (and Slightly Mad) Adventure - 2025-2026 Itinerary",
        'nav_home': "Home Base",
        'nav_protagonists': "Heroes (or Villains?)",
        'nav_adventure': "The Odyssey",
        'nav_equipment': "Gear & Dreams",
        'nav_map': "Treasure Map",
        'nav_blog': "Logbook", # AGGIUNTO PER IL BLOG
        'header_title': "SaltRiders World Tour",
        'header_subtitle': "GG & Paco's incredible 2025-2026 itinerary, an epic land and ocean journey of bikepacking, surf, slow travel, and a sustainable approach to exploration!", # MODIFICATO
        'protagonists_section_title': "Our (Sorta) Heroes",
        'gg_alt_text': "GG's photo, ready for adventure",
        'gg_name': "GG - The Enthusiastic Giant",
        'gg_description': "A free spirit with an inexhaustible supply of enthusiasm (and perhaps a dash of healthy recklessness). GG faces every challenge, no matter how absurd, with an enthusiasm that could awaken a dormant volcano. His mission: to turn every day into a memorable adventure, collecting friends and improbable anecdotes.",
        'paco_alt_text': "Paco's Photo, lost in the mountains",
        'paco_name': "Paco - The Sagacious Explorer",
        'paco_description': "A sharp mind and energetic soul, Paco is the organizing spirit of the duo. Always ready to find ingenious solutions (or at least, ones that seem so at the time), he faces every mishap with a healthy dose of creative problem-solving. The adrenaline of discovery guides him, turning every unforeseen event into… well, another unforeseen event to solve.",
        'adventure_section_title': "Our Glorious Odyssey",
        'ocean_crossing_alt': "Sailboat on an ocean crossing under a blue sky",
        'ocean_crossing_caption': "The vastness of the ocean awaits us: our next great challenge.",
        'adventure_intro1': "Fasten your seatbelts! We SaltRiders, GG and Paco, are about to embark on an odyssey that will redefine the very concept of exploration... or at least, we'll give it a stylish shot. From the beating heart of Europe, these two intrepid adventurers will unleash their trusty bikes and surfboards on a land-and-sea tour de force, ready to collect exotic cultures and postcard-perfect vistas, all while being mindful of the environment and local communities.", # MODIFICATO
        'adventure_intro2': "Their travel philosophy? More than a plan, it's a manifesto for **slow travel** and **sustainability**. A declaration of intent that embraces the unexpected, resourcefulness, and a deep connection with places and people, prioritizing human power and low-impact transport to navigate the world, avoiding air travel as much as possible.", # MODIFICATO
        'adventure_step1_title': "Europe Express, with Champion-like Poise",
        'adventure_step1_desc': "From Milan, a 'soft' start westward by rail, savouring the Old Continent at a pace that allows us to truly connect with the landscapes, before the real chaos begins.", # MODIFICATO
        'adventure_step2_title': "Epic (and Possibly Ill-Advised) Climbs",
        'adventure_step2_desc': "A 'brilliant' cycling kick-off from Turin, featuring the Herculean (and let's be honest, utterly bonkers) challenge of conquering a major Alpine pass with surfboards in tow, before (hopefully, with all bones intact) gliding into Grenoble. Who in their right mind would do this? We would! A more conventional overland transfer will then whisk us to San Sebastián, where the call of the open road will once again beckon our wheels.", # MODIFICATO
        'adventure_step3_title': "Riding the Iberian Atlantic (and the Hills)",
        'adventure_step3_desc': "Cycling like there's no tomorrow from San Sebastián along the wild coasts of Spain and Portugal, on the hunt for epic spots, perfect waves, and possibly, a place to pitch the tent.",
        'adventure_step4_title': "Caribbean Bound",
        'adventure_step4_desc': "From Las Palmas de Gran Canaria, we'll sneak into the ARC (Atlantic Rally for Cruisers) fleet on November 23, 2025. The mission: to find a passage directly on the pontoons or through unlikely contacts. Ready to cross the Atlantic, sailing towards Saint Lucia, hoping not to end up washing dishes for the entire voyage.",
        'adventure_step5_title': "Pacific Dream: Two Destinies, Same Madness",
        'adventure_step5_optionA_title': "Option A - Ocean Crossing for True (or almost) Sea Dogs",
        'adventure_step5_optionA_desc': "From the Caribbean, a 'quick' sea passage to Panama. From there, the vastness of the Pacific: an adventure of pure sailing towards gems like the Galápagos and the islands of French Polynesia, relying on the kindness of waves, winds, and anyone with a spare bunk.",
        'adventure_step5_optionB_title': "Option B - South American Roots and Calves of Steel",
        'adventure_step5_optionB_desc': "A sea passage from the Caribbean to Ecuador will mark the beginning of a LONG cycling journey. Down the Pacific coast of South America, chasing legendary waves, crossing deserts straight out of a western movie, and mountains that will test even the most stoic. An immersion into the continent's vibrant heart all the way to Chile, or until our legs give out.", # MODIFICATO
        'adventure_outro': "Forget rigid schedules: this is more a manifesto for travel lived with an indomitable spirit and awareness, a toast to the unexpected becoming the norm, to an exploration that respects the rhythms of nature and cultures, and a tribute to every single, quirky, wonderful human connection. Stay tuned, because the best (and most hilariously unpredictable parts) are yet to come!", # MODIFICATO
        'equipment_section_title': "The Dreamers' Arsenal: Bikes, Surfboards & Tent",
        'equipment_desc1': "The essence of such a unique adventure lies also in the genius of simplicity and a touch of adaptability. To tackle the long coastal stretches, we SaltRiders have chosen gravel bikes equipped with dedicated side racks to carry our beloved surfboards. This ingenious system allows us to be as agile as gazelles (though loaded like mules) and fully experience the human-and-board-scaled journey.", # MODIFICATO
        'equipment_desc2': "The rack is lightweight yet sturdy, and if the crosswinds make themselves felt... well, that's part of the adventure. We also carry a compact tent, to stop wherever we fancy and sleep under the stars, ready to set off at dawn with our faithful wave-riding companion always by our side, like a somewhat lopsided but indispensable aerodynamic appendage.", # MODIFICATO
        'equipment_image_alt': "Bikepacking with a surfboard: the SaltRiders essence!",
        'equipment_image_caption': "Our setup as SaltRiders: bike, board, and endless horizons.",
        'grizl_image_alt': "Grizl gravel bike ready for adventure on dirt roads",
        'grizl_image_caption': "Our trusty two-wheeled companion, ready to tackle any type of terrain.",
        'map_section_title': "The Interactive Journey Map",
        'footer_text': "© 2024 SaltRiders Epic Fails & Adventures - GG & Paco. Map generated with Folium (and a lot of patience). Stay Stoked (and cross your fingers for us)!",
        'map_tile_clear': "Clear Map",
        'map_tile_standard': "Standard Map",
        'map_tile_satellite': "Satellite Map",
        'map_main_group': "Main Route (Theoretical)",
        'map_planA_group': "Pacific Option: Ocean Crossing",
        'map_planB_group': "Pacific Option: South America Bike Tour",
        'map_milan_popup': "Milan - The madness begins!", 'map_milan_date': "10 Sep 25",
        'map_turin_popup': "Turin - Ready for the Alps?!", 'map_turin_date': "10 Sep 25",
        'map_train_tooltip': "Train Milan→Turin (10 Sep 25) - The warm-up",
        'map_turin_bike_popup': "Turin - Bike Start (and Alpine suffering)",
        'map_grenoble_popup': "Grenoble - Survived the Alps!", 'map_grenoble_date': "11 Sep 25",
        'map_bike1_tooltip': "Bike Turin→Grenoble (10-11 Sep 25) - 'A walk in the park,' they said...",
        'map_grenoble_bus_popup': "Grenoble - Tactical bus break", 'map_grenoble_bus_date': "11 Sep 25",
        'map_sanseb_bus_popup': "San Sebastián - We're back!", 'map_sanseb_bus_date': "12 Sep 25",
        'map_bus_tooltip': "Bus Grenoble→San Sebastián (11-12 Set 25) - Temporary civilization",
        'map_sanseb_bike_popup': "San Sebastián - Back on the bikes, coastal style!",
        'map_iberia_bike_tooltip': "Bike Iberian Atlantic Coast (14 Sep - 28 Oct 25) - Legs, waves, and tapas",
        'map_faro_sail_popup': "Faro - Seeking passage across the Atlantic", 'map_faro_sail_date': "29 Oct 25",
        'map_las_palmas_popup': "Las Palmas, Gran Canaria - Pronti per l'ARC (o quasi)", 'map_las_palmas_date': "23 Nov 25",
        'map_sail_canaries_tooltip': "Sail Faro→Las Palmas (29 Oct - 03 Nov 25) - Atlantic training",
        'map_canaries_stop_tooltip': "Stopover & ARC (panic?) preps in Gran Canaria\n03 Nov - 23 Nov 25",
        'map_st_lucia_popup': "Saint Lucia, Caribbean - Land Ho! (Finally)", 'map_st_lucia_date': "10-15 Dic 25",
        'map_arc_tooltip': "ARC: Atlantic Crossing (23 Nov - 10/15 Dic 25) - Waves, stars, and seasickness",
        'map_caribbean_explore_tooltip': "Caribbean Exploration (and energy recovery)\n15 Dic 25 - 15 Feb 26",
        'map_panama_transfer_popup': "Panama City - To the Big Blue (Pacific)", 'map_panama_transfer_date': "16 Feb 26",
        'map_sea_transfer_panama_tooltip': "Sea Passage Caribbean→Panama (Feb 26) - Switching oceans!",
        'map_panama_prep_tooltip': "Preparations in Panama (and treasure map hunting)\n16 Feb - 28 Feb 26",
        'map_panama_pacific_start_popup': "Panama - Pacific Crossing Start (All aboard!)", 'map_panama_pacific_start_date': "01 Mar 26",
        'map_sail_leg_tooltip_prefix': "Sail",
        'map_stopover_tooltip_prefix': "Stopover at",
        'map_ecuador_transfer_popup': "Guayaquil, Ecuador - South American Adventure Start",
        'map_ecuador_transfer_date': "16 Feb 26",
        'map_sea_transfer_ecuador_tooltip': "Passaggio via mare Caraibi→Ecuador (Feb 26) - Rotta a Sud!",
        'map_ecuador_explore_tooltip': "Esplorazione Ecuador (e acclimatamento)\n16 Feb - 01 Mar 26",
        'map_guayaquil_bike_popup': "Guayaquil - Inizio Bike Pacifica (e che il dio del ciclismo ci assista)",
        'map_bike_pacific_tooltip': "Bike Costa Pacifica (Mar - Lug 26) - Chilometri, sudore e panorami",
        'map_finisterre_name': "Finisterre", 'map_porto_name': "Porto", 'map_ericeira_name': "Ericeira", 'map_lisbon_name': "Lisbona", 'map_sagres_name': "Sagres", 'map_faro_name': "Faro",
        'map_galapagos_name': "Galápagos", 'map_marquesas_name': "Marchesi", 'map_tahiti_name': "Tahiti",
        'map_montanita_name': "Montañita", 'map_lobitos_name': "Lobitos", 'map_lima_name': "Lima", 'map_iquique_name': "Iquique", 'map_pichilemu_name': "Pichilemu",
        'map_fullscreen_title': "Schermo Intero (Modalità Cinema)",
        'map_fullscreen_cancel': "Esci da Schermo Intero (Ritorno alla Realtà)",
        'map_locate_title': "Dove Diavolo Sono?",
        'map_locate_popup': "Sei qui (più o meno... speriamo)",
    },
    'en': {
        'lang_code': 'en',
        'page_title': "SaltRiders: GG & Paco's Epic (and Slightly Mad) Adventure - 2025-2026 Itinerary",
        'nav_home': "Home Base",
        'nav_protagonists': "Heroes (or Villains?)",
        'nav_adventure': "The Odyssey",
        'nav_equipment': "Gear & Dreams",
        'nav_map': "Treasure Map",
        'nav_blog': "Logbook", # AGGIUNTO PER IL BLOG
        'header_title': "SaltRiders World Tour",
        'header_subtitle': "GG & Paco's incredible 2025-2026 itinerary, an epic land and ocean journey of bikepacking, surf, slow travel, and a sustainable approach to exploration!", # MODIFICATO
        'protagonists_section_title': "Our (Sorta) Heroes",
        'gg_alt_text': "GG's photo, ready for adventure",
        'gg_name': "GG - The Enthusiastic Giant",
        'gg_description': "A free spirit with an inexhaustible supply of enthusiasm (and perhaps a dash of healthy recklessness). GG faces every challenge, no matter how absurd, with an enthusiasm that could awaken a dormant volcano. His mission: to turn every day into a memorable adventure, collecting friends and improbable anecdotes.",
        'paco_alt_text': "Paco's Photo, lost in the mountains",
        'paco_name': "Paco - The Sagacious Explorer",
        'paco_description': "A sharp mind and energetic soul, Paco is the organizing spirit of the duo. Always ready to find ingenious solutions (or at least, ones that seem so at the time), he faces every mishap with a healthy dose of creative problem-solving. The adrenaline of discovery guides him, turning every unforeseen event into… well, another unforeseen event to solve.",
        'adventure_section_title': "Our Glorious Odyssey",
        'ocean_crossing_alt': "Sailboat on an ocean crossing under a blue sky",
        'ocean_crossing_caption': "The vastness of the ocean awaits us: our next great challenge.",
        'adventure_intro1': "Fasten your seatbelts! We SaltRiders, GG and Paco, are about to embark on an odyssey that will redefine the very concept of exploration... or at least, we'll give it a stylish shot. From the beating heart of Europe, these two intrepid adventurers will unleash their trusty bikes and surfboards on a land-and-sea tour de force, ready to collect exotic cultures and postcard-perfect vistas, all while being mindful of the environment and local communities.", # MODIFICATO
        'adventure_intro2': "Their travel philosophy? More than a plan, it's a manifesto for **slow travel** and **sustainability**. A declaration of intent that embraces the unexpected, resourcefulness, and a deep connection with places and people, prioritizing human power and low-impact transport to navigate the world, avoiding air travel as much as possible.", # MODIFICATO
        'adventure_step1_title': "Europe Express, with Champion-like Poise",
        'adventure_step1_desc': "From Milan, a 'soft' start westward by rail, savouring the Old Continent at a pace that allows us to truly connect with the landscapes, before the real chaos begins.", # MODIFICATO
        'adventure_step2_title': "Epic (and Possibly Ill-Advised) Climbs",
        'adventure_step2_desc': "A 'brilliant' cycling kick-off from Turin, featuring the Herculean (and let's be honest, utterly bonkers) challenge of conquering a major Alpine pass with surfboards in tow, before (hopefully, with all bones intact) gliding into Grenoble. Who in their right mind would do this? We would! A more conventional overland transfer will then whisk us to San Sebastián, where the call of the open road will once again beckon our wheels.", # MODIFICATO
        'adventure_step3_title': "Riding the Iberian Atlantic (and the Hills)",
        'adventure_step3_desc': "Cycling like there's no tomorrow from San Sebastián along the wild coasts of Spain and Portugal, on the hunt for epic spots, perfect waves, and possibly, a place to pitch the tent.",
        'adventure_step4_title': "Caribbean Bound",
        'adventure_step4_desc': "From Las Palmas de Gran Canaria, we'll sneak into the ARC (Atlantic Rally for Cruisers) fleet on November 23, 2025. The mission: to find a passage directly on the pontoons or through unlikely contacts. Ready to cross the Atlantic, sailing towards Saint Lucia, hoping not to end up washing dishes for the entire voyage.",
        'adventure_step5_title': "Pacific Dream: Two Destinies, Same Madness",
        'adventure_step5_optionA_title': "Option A - Ocean Crossing for True (or almost) Sea Dogs",
        'adventure_step5_optionA_desc': "From the Caribbean, a 'quick' sea passage to Panama. From there, the vastness of the Pacific: an adventure of pure sailing towards gems like the Galápagos and the islands of French Polynesia, relying on the kindness of waves, winds, and anyone with a spare bunk.",
        'adventure_step5_optionB_title': "Option B - South American Roots and Calves of Steel",
        'adventure_step5_optionB_desc': "A sea passage from the Caribbean to Ecuador will mark the beginning of a LONG cycling journey. Down the Pacific coast of South America, chasing legendary waves, crossing deserts straight out of a western movie, and mountains that will test even the most stoic. An immersion into the continent's vibrant heart all the way to Chile, or until our legs give out.", # MODIFICATO
        'adventure_outro': "Forget rigid schedules: this is more a manifesto for travel lived with an indomitable spirit and awareness, a toast to the unexpected becoming the norm, to an exploration that respects the rhythms of nature and cultures, and a tribute to every single, quirky, wonderful human connection. Stay tuned, because the best (and most hilariously unpredictable parts) are yet to come!", # MODIFICATO
        'equipment_section_title': "The Dreamers' Arsenal: Bikes, Surfboards & Tent",
        'equipment_desc1': "The essence of such a unique adventure lies also in the genius of simplicity and a touch of adaptability. To tackle the long coastal stretches, we SaltRiders have chosen gravel bikes equipped with dedicated side racks to carry our beloved surfboards. This ingenious system allows us to be as agile as gazelles (though loaded like mules) and fully experience the human-and-board-scaled journey.", # MODIFICATO
        'equipment_desc2': "The rack is lightweight yet sturdy, and if the crosswinds make themselves felt... well, that's part of the adventure. We also carry a compact tent, to stop wherever we fancy and sleep under the stars, ready to set off at dawn with our faithful wave-riding companion always by our side, like a somewhat lopsided but indispensable aerodynamic appendage.", # MODIFICATO
        'equipment_image_alt': "Bikepacking with a surfboard: the SaltRiders essence!",
        'equipment_image_caption': "Our setup as SaltRiders: bike, board, and endless horizons.",
        'grizl_image_alt': "Grizl gravel bike ready for adventure on dirt roads",
        'grizl_image_caption': "Our trusty two-wheeled companion, ready to tackle any type of terrain.",
        'map_section_title': "The Interactive Journey Map",
        'footer_text': "© 2024 SaltRiders Epic Fails & Adventures - GG & Paco. Map generated with Folium (and a lot of patience). Stay Stoked (and cross your fingers for us)!",
        'map_tile_clear': "Clear Map",
        'map_tile_standard': "Standard Map",
        'map_tile_satellite': "Satellite Map",
        'map_main_group': "Main Route (Theoretical)",
        'map_planA_group': "Pacific Option: Ocean Crossing",
        'map_planB_group': "Pacific Option: South America Bike Tour",
        'map_milan_popup': "Milan - The madness begins!", 'map_milan_date': "10 Sep 25",
        'map_turin_popup': "Turin - Ready for the Alps?!", 'map_turin_date': "10 Sep 25",
        'map_train_tooltip': "Train Milan→Turin (10 Sep 25) - The warm-up",
        'map_turin_bike_popup': "Turin - Bike Start (and Alpine suffering)",
        'map_grenoble_popup': "Grenoble - Survived the Alps!", 'map_grenoble_date': "11 Sep 25",
        'map_bike1_tooltip': "Bike Turin→Grenoble (10-11 Sep 25) - 'A walk in the park,' they said...",
        'map_grenoble_bus_popup': "Grenoble - Tactical bus break", 'map_grenoble_bus_date': "11 Sep 25",
        'map_sanseb_bus_popup': "San Sebastián - We're back!", 'map_sanseb_bus_date': "12 Sep 25",
        'map_bus_tooltip': "Bus Grenoble→San Sebastián (11-12 Sep 25) - Temporary civilization",
        'map_sanseb_bike_popup': "San Sebastián - Back on the bikes, coastal style!",
        'map_iberia_bike_tooltip': "Bike Iberian Atlantic Coast (14 Sep - 28 Oct 25) - Legs, waves, and tapas",
        'map_faro_sail_popup': "Faro - Seeking passage across the Atlantic", 'map_faro_sail_date': "29 Oct 25",
        'map_las_palmas_popup': "Las Palmas, Gran Canaria - ARC ready (almost)", 'map_las_palmas_date': "23 Nov 25",
        'map_sail_canaries_tooltip': "Sail Faro→Las Palmas (29 Oct - 03 Nov 25) - Atlantic training",
        'map_canaries_stop_tooltip': "Stopover & ARC (panic?) preps in Gran Canaria\n03 Nov - 23 Nov 25",
        'map_st_lucia_popup': "Saint Lucia, Caribbean - Land Ho! (Finally)", 'map_st_lucia_date': "10-15 Dic 25",
        'map_arc_tooltip': "ARC: Atlantic Crossing (23 Nov - 10/15 Dic 25) - Waves, stars, and seasickness",
        'map_caribbean_explore_tooltip': "Caribbean Exploration (and energy recovery)\n15 Dic 25 - 15 Feb 26",
        'map_panama_transfer_popup': "Panama City - To the Big Blue (Pacific)", 'map_panama_transfer_date': "16 Feb 26",
        'map_sea_transfer_panama_tooltip': "Sea Passage Caribbean→Panama (Feb 26) - Switching oceans!",
        'map_panama_prep_tooltip': "Preparations in Panama (and treasure map hunting)\n16 Feb - 28 Feb 26",
        'map_panama_pacific_start_popup': "Panama - Pacific Crossing Start (All aboard!)", 'map_panama_pacific_start_date': "01 Mar 26",
        'map_sail_leg_tooltip_prefix': "Sail",
        'map_stopover_tooltip_prefix': "Stopover at",
        'map_ecuador_transfer_popup': "Guayaquil, Ecuador - South American Adventure Start",
        'map_ecuador_transfer_date': "16 Feb 26",
        'map_sea_transfer_ecuador_tooltip': "Sea Passage Caribbean→Ecuador (Feb 26) - Rotta a Sud!",
        'map_ecuador_explore_tooltip': "Ecuador Exploration (and acclimatamento)\n16 Feb - 01 Mar 26",
        'map_guayaquil_bike_popup': "Guayaquil - Inizio Bike Pacifica (e che il dio del ciclismo ci assista)",
        'map_bike_pacific_tooltip': "Bike Costa Pacifica (Mar - Lug 26) - Chilometri, sudore e panorami",
        'map_finisterre_name': "Finisterre", 'map_porto_name': "Porto", 'map_ericeira_name': "Ericeira", 'map_lisbon_name': "Lisbona", 'map_sagres_name': "Sagres", 'map_faro_name': "Faro",
        'map_galapagos_name': "Galápagos", 'map_marquesas_name': "Marchesi", 'map_tahiti_name': "Tahiti",
        'map_montanita_name': "Montañita", 'map_lobitos_name': "Lobitos", 'map_lima_name': "Lima", 'map_iquique_name': "Iquique", 'map_pichilemu_name': "Pichilemu",
        'map_fullscreen_title': "Schermo Intero (Modalità Cinema)",
        'map_fullscreen_cancel': "Esci da Schermo Intero (Ritorno alla Realtà)",
        'map_locate_title': "Dove Diavolo Sono?",
        'map_locate_popup': "Sei qui (più o meno... speriamo)",
    }
}

# --- Dati per la Mappa ---
MAP_DATA_COORDS = {
    'train_pts': [(45.4642, 9.1900), (45.0703, 7.6869)],
    'bike1_pts': [(45.0703, 7.6869), (45.1885, 5.7245)],
    'bus_pts': [(45.1885, 5.7245), (43.3183, -1.9812)],
    'iberia_start_coord': (43.3183, -1.9812),
    'iberia_coords': [
        (43.3183, -1.9812), (42.8800, -9.3000), (41.1500, -8.6300),
        (39.5000, -9.1300), (38.7200, -9.1400), (37.0200, -8.9300),
        (37.0179, -7.9307)
    ],
    'iberia_names_keys': [
        "map_sanseb_bike_popup", "map_finisterre_name", "map_porto_name",
        "map_ericeira_name", "map_lisbon_name", "map_sagres_name", "map_faro_name"
    ],
    'iberia_dates_str': [
        "14 Set 25", "30 Sep 25", "10 Oct 25", "15 Oct 25",
        "20 Oct 25", "25 Oct 25", "28 Oct 25"
    ],
    'faro_coord': (37.0179, -7.9307),
    'las_palmas_coord_simple': (28.1234, -15.4362),
    'sail_to_canaries_pts': [(37.0179, -7.9307), (28.1234, -15.4362)],
    'st_lucia_coord_simple': (14.0108, -60.9707),
    'arc_pts': [(28.1234, -15.4362), (14.0108, -60.9707)],
    'panama_city_coord': (9.0000, -79.5000),
    'sea_to_panama_pts': [(14.0108, -60.9707), (9.0000, -79.5000)],
    'cross_pacific_coords': [
        (9.0000, -79.5000), (-0.9000, -89.6000),
        (-9.8000, -139.0000), (-17.5500, -149.5600)
    ],
    'cross_pacific_names_keys': [
        "map_panama_pacific_start_popup", "map_galapagos_name",
        "map_marquesas_name", "map_tahiti_name"
    ],
    'cross_pacific_arrival_dates_str': ["N/A", "10 Mar 26", "30 Apr 26", "15 Jun 26"],
    'ecuador_coast_approx': (-2.1700, -79.9000),
    'sea_to_ecuador_pts': [(14.0108, -60.9707), (-2.1700, -79.9000)],
    'bike_southam_coords': [
        (-2.1700, -79.9000), (-1.8300, -80.7500), (-4.4400, -81.2800),
        (-12.0500, -77.0400), (-20.2300, -70.1400), (-34.3800, -72.0000)
    ],
    'bike_southam_names_keys': [
        "map_guayaquil_bike_popup", "map_montanita_name", "map_lobitos_name",
        "map_lima_name", "map_iquique_name", "map_pichilemu_name"
    ],
    'bike_southam_dates_str': [
        "01 Mar 26", "15 Apr 26", "15 May 26", "15 Jun 26",
        "01 Jul 26", "30 Jul 26"
    ]
}

# --- Percorsi ---
BASE_OUTPUT_DIR = "."
IMAGES_DIR_NAME = "images"
CSS_DIR_NAME = "css"
BLOG_POSTS_DIR = "_posts"
BLOG_OUTPUT_DIR_BASE = "blog"

# --- Nomi file immagini (il prefisso di lingua sarà gestito nello script principale) ---
GG_PHOTO_FILENAME = "gg1.jpeg"
PACO_PHOTO_FILENAME = "paco.jpeg"
SURF_PHOTO_URL_EXTERNAL = "https://www.thejambo.it/wp-content/uploads/2023/05/Le-migliori-destinazioni-al-mondo-per-fare-surf-Foto-di-Canva-3-1024x683.png"
BIKE_SETUP_PHOTO_FILENAME = "surfpacking1.jpg"
GRIZL_PHOTO_FILENAME = "grizl.jpg"
OCEAN_CROSSING_PHOTO_FILENAME = "ocean_crossing.jpg"

# --- Template per il Blog ---
BLOG_COMMON_CSS_FILENAME = "blog_style.css"

BLOG_POST_TEMPLATE_STR = """
<!DOCTYPE html>
<html lang="{{ post.lang }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ post.title }} - SaltRiders Blog</title>
    <link rel="stylesheet" href="{{ post.get_css_path(post.css_common_filename) }}">
</head>
<body>
    <div class="blog-page-container single-post-page">
        <header class="blog-header single-post-header">
            <nav class="blog-nav">
                <a href="{{ post.get_main_site_url() }}">Sito Principale SaltRiders</a>
                <a href="{{ post.blog_index_url }}">Indice del Blog</a>
            </nav>
            <h1>{{ post.title }}</h1>
            <p class="single-post-meta">
                Pubblicato il: <time datetime="{{ post.date }}">{{ post.date }}</time> 
                {% if post.author %}da {{ post.author }}{% endif %}
            </p>
        </header>

        <main>
            {% if post.image %}
            <figure class="single-post-featured-image">
                <img src="{{ post.get_image_path(post.image) }}" alt="Immagine di copertina per {{ post.title }}">
            </figure>
            {% endif %}

            <article class="single-post-content">
                {{ post.content_html | safe }}
            </article>
        </main>


        <footer class="blog-footer">
            <p>© SaltRiders Adventures</p>
        </footer>
    </div>
</body>
</html>
"""

BLOG_INDEX_TEMPLATE_STR = """
<!DOCTYPE html>
<html lang="{{ lang_code }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SaltRiders Blog - {{ lang_code.upper() }}</title>
    <link rel="stylesheet" href="{{ get_css_path(css_common_filename) }}">
    <!-- Non servono stili inline qui se usiamo bene blog_style.css -->
</head>
<body>
    <div class="blog-index-page"> <!-- Contenitore specifico per la pagina indice -->
        <header class="blog-header blog-index-header">
            <nav class="blog-nav">
                <a href="{{ main_site_url() }}">Sito Principale SaltRiders</a>
            </nav>
            <h1>SaltRiders Blog <span class="lang-indicator">({{ lang_code.upper() }})</span></h1>
            <p class="blog-index-subtitle">Cronache, avventure e riflessioni dal nostro viaggio intorno al mondo.</p>
        </header>

        <main class="blog-container blog-post-grid">
            {% if posts %}
                {% for post in posts %}
                <article class="blog-post-card">
                    <a href="{{ post.url }}" class="card-link-wrapper">
                        {% if post.image %}
                        <div class="card-image-container">
                            <img src="{{ post.get_image_path(post.image) }}" alt="{{ post.title }}" class="card-image">
                        </div>
                        {% endif %}
                        <div class="card-content">
                            <h2 class="card-title">{{ post.title }}</h2>
                            <p class="blog-post-meta card-meta">
                                <span class="meta-date">{{ post.date }}</span>
                                {% if post.author %}<span class="meta-author">di {{ post.author }}</span>{% endif %}
                            </p>
                            <p class="card-summary">{{ post.summary }}</p>
                            <span class="read-more-card-link">Leggi l'articolo →</span>
                        </div>
                    </a>
                </article>
                {% endfor %}
            {% else %}
                <p class="no-posts-message">Nessun post trovato in questa lingua per ora. L'avventura è appena iniziata, torna presto!</p>
            {% endif %}
        </main>

        <footer class="blog-footer">
            <p>© SaltRiders Adventures</p>
        </footer>
    </div>
</body>
</html>
"""