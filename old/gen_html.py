import os
import folium
from folium import plugins
from folium.features import DivIcon
from jinja2 import Template
from datetime import datetime, timedelta

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

        /* === MAP CONTAINER STYLES (MODIFIED) === */
        #map-container {
            width: 100%;
            /* Obiettivo altezza: 70% della viewport, ma non meno di 350px e non più di 600px */
            height: clamp(350px, 70vh, 600px); /* Combina min, valore preferito, max */
            border-radius: 18px;
            overflow: hidden; 
            box-shadow: 0 12px 35px rgba(0,0,0,0.08);
            margin-top: 35px; 
            background-color: #e0e0e0; /* Sfondo di fallback se la mappa carica lentamente */
            position: relative; 
            /* Aggiunta per performance: dice al browser che questo elemento cambierà trasformazioni/opacità
               e può essere ottimizzato separatamente dal resto del flusso del documento. */
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
        /* === END MAP CONTAINER STYLES === */

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

        @media (max-width: 991.98px) { /* Breakpoint lg di Bootstrap per il collapse */
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

            /* Altezza mappa specifica per mobile con clamp */
            #map-container { 
                /* Obiettivo 55vh, min 300px, max 450px su mobile */
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
    <!-- ^ Assicurati che jQuery sia caricato prima dei plugin se lo usano, ma Leaflet no -->

    <script src="https://cdnjs.cloudflare.com/ajax/libs/Leaflet.awesome-markers/2.0.2/leaflet.awesome-markers.js"></script>
    <script src="https://cdn.jsdelivr.net/gh/marslan390/BeautifyMarker/leaflet-beautify-marker-icon.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/leaflet.fullscreen@3.0.0/Control.FullScreen.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet-minimap/3.6.1/Control.MiniMap.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet-locatecontrol/0.66.2/L.Control.Locate.min.js"></script>

    <script>
        // Funzione per eseguire il codice quando il DOM è pronto, ma prima del completo caricamento di immagini ecc.
        function onDocumentReady(fn) {
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', fn);
            } else {
                fn(); // DOM già pronto
            }
        }

        // Funzione per eseguire il codice quando l'intera pagina è caricata (immagini, script, ecc.)
        function onWindowLoad(fn) {
            if (document.readyState === 'complete') {
                fn(); // Già caricata
            } else {
                window.addEventListener('load', fn);
            }
        }

        var leafletMapInstances = []; // Array per memorizzare le istanze della mappa

        function invalidateAllMapsSize() {
            leafletMapInstances.forEach(function(mapInstance) {
                if (mapInstance && typeof mapInstance.invalidateSize === 'function') {
                    mapInstance.invalidateSize({ animate: false });
                }
            });
        }

        // Funzione opzionale per adattare i bounds, se necessaria
        // function fitMapBoundsToContent(mapInstance) {
        //     if (!mapInstance) return;
        //     // Definisci qui i bounds che vuoi mostrare. Esempio:
        //     // var southWest = L.latLng(-40, -95);
        //     // var northEast = L.latLng(60, 25);
        //     // var bounds = L.latLngBounds(southWest, northEast);
        //     // if (bounds.isValid()) {
        //     //    mapInstance.fitBounds(bounds, { padding: L.point(25, 25), maxZoom: 10 });
        //     // } else {
        //     //    mapInstance.setView([20,0], 2); // Fallback view
        //     // }
        // }

        function initializeMapLogic() {
            if (typeof L !== 'undefined') {
                var mapDivs = document.querySelectorAll('#map-container .folium-map');
                mapDivs.forEach(function(div) {
                    if (div._leaflet_map && leafletMapInstances.indexOf(div._leaflet_map) === -1) {
                        leafletMapInstances.push(div._leaflet_map);
                    }
                });

                // Invalida le dimensioni subito dopo aver trovato le istanze.
                // Il CSS con clamp() dovrebbe fornire dimensioni stabili prima.
                invalidateAllMapsSize();

                // Se usi fitBounds, chiamalo qui dopo invalidateSize
                // leafletMapInstances.forEach(fitMapBoundsToContent);
            }
        }

        onDocumentReady(function () {
            // Inizializza la logica della mappa non appena il DOM è pronto.
            // Questo è importante perché Folium inserisce la mappa direttamente nell'HTML.
            initializeMapLogic();

            // Logica per la navbar e lo smooth scroll (già presente, mantenuta)
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

            // Logica per Intersection Observer (già presente, mantenuta)
            const sections = document.querySelectorAll('.header-banner, .content-section');
            const observerOptions = {
                root: null,
                rootMargin: "0px 0px -40% 0px", // Cambiato leggermente per reattività
                threshold: 0.05 // Ridotto per attivare prima l'effetto visible e il link attivo
            };
             const sectionObserver = new IntersectionObserver((entries, observer) => {
                let intersectingEntry = null;
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                         // Se più entry sono isIntersecting, prendi quella più in alto nella viewport o più visibile
                        if (!intersectingEntry || entry.boundingClientRect.top < intersectingEntry.boundingClientRect.top || entry.intersectionRatio > intersectingEntry.intersectionRatio) {
                            intersectingEntry = entry;
                        }
                    }
                    // Rendi visibile la sezione se entra (anche parzialmente)
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

                    if (rect.top < window.innerHeight - navbarHeight && rect.bottom > navbarHeight) { // È visibile?
                        if (section.id === 'home' && rect.top <= navbarHeight + 5) { // Home è vicina alla cima?
                            firstVisibleSectionId = 'home';
                            maxVisibility = Infinity; // Dagli priorità assoluta
                            break; 
                        }
                        if (maxVisibility !== Infinity) { // Se home non ha già vinto
                            if (rect.top < (document.getElementById(firstVisibleSectionId)?.getBoundingClientRect().top || Infinity) ) {
                                firstVisibleSectionId = section.id;
                            }
                        }
                    }
                     // Rendi visibile la prima sezione al caricamento se non già fatto da observer
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
            // Esegui dopo un breve ritardo per permettere al layout di stabilizzarsi
            setTimeout(setActiveLinkOnLoad, 150); 
        });

        // Listener aggiuntivi per resize e visibility change su window.load
        // per assicurarsi che la mappa sia completamente pronta
        onWindowLoad(function() {
            // Potrebbe essere necessario un secondo invalidate dopo che tutto (immagini ecc.) è caricato
            // se le dimensioni del contenitore mappa dipendono da esse.
            setTimeout(invalidateAllMapsSize, 100); 

            var resizeDebounceTimeout;
            window.addEventListener('resize', function() {
                clearTimeout(resizeDebounceTimeout);
                resizeDebounceTimeout = setTimeout(function() {
                    invalidateAllMapsSize();
                    // leafletMapInstances.forEach(fitMapBoundsToContent); // Se usi fitBounds
                }, 250); 
            });

            document.addEventListener('visibilitychange', function() {
                if (document.visibilityState === 'visible') {
                    setTimeout(function() {
                        invalidateAllMapsSize();
                        // leafletMapInstances.forEach(fitMapBoundsToContent); // Se usi fitBounds
                    }, 200); 
                }
            });
        });
    </script>
</body>
</html>
"""

# --- Testi (INVARIATI) ---
text_content = {
    'it': {
        'lang_code': 'it',
        'page_title': "SaltRiders: L'Avventura Epica (e un po' Folle) di GG & Paco - Itinerario 2025-2026",
        'nav_home': "Home",
        'nav_protagonists': "Eroi (o Anti-Eroi?)",
        'nav_adventure': "L'Odissea",
        'nav_equipment': "Ferraglia & Sogni",
        'nav_map': "La Mappa del Tesoro",
        'header_title': "SaltRiders World Tour",
        'header_subtitle': "L'incredibile itinerario 2025-2026 di GG & Paco, un'epopea via terra e mare all'insegna del bikepacking e del surf",
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
        'adventure_intro1': "Allacciate le cinture (o meglio, stringete le cinghie dei portapacchi)! I SaltRiders, GG e Paco, stanno per intraprendere un'odissea che riscriverà le regole dell'esplorazione... o almeno, ci proveranno con stile. Dal cuore pulsante dell'Europa, questi due intrepidi (o incoscienti?) avventurieri scateneranno le loro fidate bici e tavole da surf in un tour de force via terra e mare, pronti a collezionare culture esotiche e panorami da cartolina.",
        'adventure_intro2': "La loro filosofia di viaggio? Più che un piano, una dichiarazione d'intenti, aperta all'imprevisto e all'ingegno:",
        'adventure_step1_title': "Europa Express, con la Calma dei Campioni",
        'adventure_step1_desc': "Da Milano, un inizio 'soft' su rotaia verso ovest, giusto per assaporare il Vecchio Continente prima del vero caos.",
        'adventure_step2_title': "Scalate Epiche (e Forse Poco Sensate)",
        'adventure_step2_desc': "Un avvio in bicicletta da Torino, con l'ardua impresa di valicare un importante passo alpino con tavole al seguito, per planare (si spera con tutte le ossa intere) su Grenoble. Chi sano di mente lo farebbe? Noi! Seguirà un trasferimento via terra più convenzionale verso San Sebastián, dove l'asfalto tornerà a chiamare le loro ruote.",
        'adventure_step3_title': "Cavalcando l'Atlantico Iberico (e le Salite)",
        'adventure_step3_desc': "Pedalando come se non ci fosse un domani da San Sebastián lungo le coste selvagge di Spagna e Portogallo, alla ricerca di spot da urlo, onde perfette e, possibilmente, un posto dove montare la tenda.",
        'adventure_step4_title': "Rotta per i Caraibi",
        'adventure_step4_desc': "Da Las Palmas de Gran Canaria, ci intrufoleremo nella flotta dell'ARC (Atlantic Rally for Cruisers) il 23 Novembre 2025. L'obiettivo: trovare un imbarco direttamente sui pontili o tramite contatti improbabili. Pronti ad attraversare l'Atlantico veleggiando verso Saint Lucia, sperando di non finire a lavare i piatti per tutta la traversata.",
        'adventure_step5_title': "Sogno Pacifico: Due Destini, Stessa Follia",
        'adventure_step5_optionA_title': "Opzione A - Traversata Oceanica da veri Lupi di Mare (o quasi)",
        'adventure_step5_optionA_desc': "Dai Caraibi, un passaggio 'al volo' via mare per Panama. Da lì, l'immensità del Pacifico: un'avventura di pura navigazione verso perle come le Galápagos e le isole della Polinesia Francese, affidandoci al buon cuore delle onde, dei venti e di chiunque abbia una cuccetta libera.",
        'adventure_step5_optionB_title': "Opzione B - Radici Sudamericane e Polpacci d'Acciaio",
        'adventure_step5_optionB_desc': "Un passaggio marittimo dai Caraibi all'Ecuador segnerà l'inizio di una LUNGA pedalata. Giù per la costa Pacifica del Sudamerica, inseguendo onde mitiche, attraversando deserti e montagne che metteranno alla prova anche i più stoici. Un'immersione nel cuore pulsante del continente fino al Cile, o finché le gambe reggeranno.",
        'adventure_outro': "Dimenticate le tabelle di marcia precise: questo è più un manifesto al viaggio vissuto con spirito indomito, un brindisi all'imprevisto che diventa la norma e un tributo a ogni singola, strampalata, meravigliosa connessione umana. Restate sintonizzati, perché il bello deve ancora venire (e probabilmente non andrà come previsto)!",
        'equipment_section_title': "L'Arsenale dei Sognatori: Bici, Surf & Tenda",
        'equipment_desc1': "L'essenza di un'avventura così particolare risiede anche nella genialità della semplicità e in un pizzico di spirito d’adattamento. Per affrontare le lunghe tratte costiere, GG e Paco hanno scelto bici gravel equipaggiate con supporti laterali dedicati per trasportare le loro amate tavole da surf. Questo sistema ingegnoso permette loro di essere agili come gazzelle (carichi come muli) e vivere appieno l’esperienza del viaggio a misura d’uomo e di tavola.",
        'equipment_desc2': "Il supporto è leggero ma resistente, e se il vento laterale si farà sentire… fa parte dell’avventura. Con loro anche una tenda compatta, per fermarsi dove capita e dormire sotto le stelle, pronti a ripartire all’alba con la fedele compagna d’onda sempre al fianco, come un’appendice aerodinamica un po’ sbilenca ma indispensabile.",
        'equipment_image_alt': "Bikepacking con tavola da surf: l'essenza SaltRiders!",
        'equipment_image_caption': "Il nostro assetto da SaltRiders: bici, tavola e orizzonti infiniti.",
        'grizl_image_alt': "Bici gravel Grizl pronta per l'avventura su sterrato",
        'grizl_image_caption': "La nostra fidata compagna a due ruote, pronta ad affrontare ogni tipo di terreno.",
        'map_section_title': "La Mappa Interattiva",
        'footer_text': "© 2024 SaltRiders Epic Fails & Adventures - GG & Paco. Mappa generata con Folium (e tanta pazienza). Stay Stoked (e incrociate le dita per noi)!",
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
        'header_title': "SaltRiders World Tour",
        'header_subtitle': "GG & Paco's incredible 2025-2026 itinerary, an epic land and ocean journey of bikepacking and surf!",
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
        'adventure_intro1': "Fasten your seatbelts (or rather, tighten your roof rack straps)! The SaltRiders, GG and Paco, are about to embark on an odyssey that will redefine the very concept of exploration... or at least, they'll give it a stylish shot. From the beating heart of Europe, these two intrepid (or perhaps, gloriously reckless?) adventurers will unleash their trusty bikes and surfboards on a land-and-sea tour de force, ready to collect exotic cultures and postcard-perfect vistas.",
        'adventure_intro2': "Their travel philosophy? More than a plan, it's a declaration of intent, wide open to the unexpected and pure ingenuity:",
        'adventure_step1_title': "Europe Express, with Champion-like Poise",
        'adventure_step1_desc': "From Milan, a 'soft' start westward by rail, just to savour the Old Continent before the real chaos begins.",
        'adventure_step2_title': "Epic (and Possibly Ill-Advised) Climbs",
        'adventure_step2_desc': "A 'brilliant' cycling kick-off from Turin, featuring the Herculean (and let's be honest, utterly bonkers) challenge of conquering a major Alpine pass with surfboards in tow, before (hopefully, with all bones intact) gliding into Grenoble. Who in their right mind would do this? We would! A more conventional overland transfer will then whisk them to San Sebastián, where the call of the open road will once again beckon their wheels.",
        'adventure_step3_title': "Riding the Iberian Atlantic (and the Hills)",
        'adventure_step3_desc': "Cycling like there's no tomorrow from San Sebastián along the wild coasts of Spain and Portugal, on the hunt for epic spots, perfect waves, and possibly, a place to pitch the tent.",
        'adventure_step4_title': "Caribbean Bound",
        'adventure_step4_desc': "From Las Palmas de Gran Canaria, we'll sneak into the ARC (Atlantic Rally for Cruisers) fleet on November 23, 2025. The mission: to find a passage directly on the pontoons or through unlikely contacts. Ready to cross the Atlantic, sailing towards Saint Lucia, hoping not to end up washing dishes for the entire voyage.",
        'adventure_step5_title': "Pacific Dream: Two Destinies, Same Madness",
        'adventure_step5_optionA_title': "Option A - Ocean Crossing for True (or almost) Sea Dogs",
        'adventure_step5_optionA_desc': "From the Caribbean, a 'quick' sea passage to Panama. From there, the vastness of the Pacific: an adventure of pure sailing towards gems like the Galápagos and the islands of French Polynesia, relying on the kindness of waves, winds, and anyone with a spare bunk.",
        'adventure_step5_optionB_title': "Option B - South American Roots and Calves of Steel",
        'adventure_step5_optionB_desc': "A sea passage from the Caribbean to Ecuador will mark the beginning of a LONG cycling journey. Down the Pacific coast of South America, chasing legendary waves, crossing deserts straight out of a western movie, and mountains that will test even the most stoic. An immersion into the continent's vibrant heart all the way to Chile, or until their legs give out.",
        'adventure_outro': "Forget rigid schedules: this is more a manifesto for travel lived with an indomitable spirit, a toast to the unexpected becoming the norm, and a tribute to every single, quirky, wonderful human connection. Stay tuned, because the best (and most hilariously unpredictable parts) are yet to come!",
        'equipment_section_title': "The Dreamers' Arsenal: Bikes, Surfboards & Tent",
        'equipment_desc1': "The essence of such a unique adventure lies also in the genius of simplicity and a touch of adaptability. To tackle the long coastal stretches, GG and Paco have chosen gravel bikes equipped with dedicated side racks to carry their beloved surfboards. This ingenious system allows them to be as agile as gazelles (though loaded like mules) and fully experience the human-and-board-scaled journey.",
        'equipment_desc2': "The rack is lightweight yet sturdy, and if the crosswinds make themselves felt... well, that's part of the adventure. They'll also carry a compact tent, to stop wherever they fancy and sleep under the stars, ready to set off at dawn with their faithful wave-riding companion always by their side, like a somewhat lopsided but indispensable aerodynamic appendage.",
        'equipment_image_alt': "Bikepacking with a surfboard: the SaltRiders essence!",
        'equipment_image_caption': "The SaltRiders setup: bike, board, and endless horizons.",
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
        'map_st_lucia_popup': "Saint Lucia, Caribbean - Land Ho! (Finally)", 'map_st_lucia_date': "10-15 Dec 25",
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
        'map_sea_transfer_ecuador_tooltip': "Sea Passage Caribbean→Ecuador (Feb 26) - Heading South!",
        'map_ecuador_explore_tooltip': "Ecuador Exploration (and acclimatization)\n16 Feb - 01 Mar 26",
        'map_guayaquil_bike_popup': "Guayaquil - Pacific Bike Tour Start (may the cycling gods be with us)",
        'map_bike_pacific_tooltip': "Bike Pacific Coast (Mar - Jul 26) - Kilometers, sweat, and views",
        'map_finisterre_name': "Finisterre", 'map_porto_name': "Porto", 'map_ericeira_name': "Ericeira", 'map_lisbon_name': "Lisbon", 'map_sagres_name': "Sagres", 'map_faro_name': "Faro",
        'map_galapagos_name': "Galápagos", 'map_marquesas_name': "Marchesi", 'map_tahiti_name': "Tahiti",
        'map_montanita_name': "Montañita", 'map_lobitos_name': "Lobitos", 'map_lima_name': "Lima", 'map_iquique_name': "Iquique", 'map_pichilemu_name': "Pichilemu",
        'map_fullscreen_title': "Fullscreen (Cinema Mode)",
        'map_fullscreen_cancel': "Exit Fullscreen (Back to Reality)",
        'map_locate_title': "Where The Heck Am I?",
        'map_locate_popup': "You are here (more or less... hopefully)",
    }
}

# --- 1. Definizioni Dati e Funzioni Helper (INVARIATE) ---
base_output_dir = "."
os.makedirs(os.path.join(base_output_dir, "en"), exist_ok=True)
os.makedirs(os.path.join(base_output_dir, "images"), exist_ok=True)  # Assicurati che esista


def add_label(lat, lon, text, group):
    text_width = 150
    folium.Marker(
        [lat, lon],
        icon=DivIcon(
            icon_size=(text_width, 24),
            icon_anchor=(text_width // 2, -10),
            html=f'<div style="font-size:8pt; color:rgba(0,0,0,0.7); text-align:center; white-space: nowrap;">{text}</div>'
        )
    ).add_to(group)


def add_marker_custom(lat, lon, name, date, icon, color, group, lang_texts):
    popup_name = lang_texts.get(name, name)
    ico = plugins.BeautifyIcon(
        icon=icon, icon_shape='marker', background_color=color,
        border_color=color, text_color='white', prefix='fa'
    )
    folium.Marker([lat, lon], popup=popup_name, icon=ico).add_to(group)
    if date:
        # Se la data è una stringa fissa (es. "10 Set 25"), usala direttamente.
        # Altrimenti, se è una chiave per lang_texts, traducila.
        date_text = date if ' ' in date else lang_texts.get(date, date)  # Semplice controllo per data fissa vs chiave
        add_label(lat, lon, date_text, group)


def add_line_custom(points, color, dash, tooltip_key, group, lang_texts):
    tooltip_text = lang_texts.get(tooltip_key, tooltip_key)
    folium.PolyLine(points, color=color, weight=4, dash_array=dash, tooltip=tooltip_text).add_to(group)


def add_circle_custom(coords, radius, color, weight, fill, fill_color, fill_opacity, tooltip_key, group, lang_texts):
    tooltip_text = lang_texts.get(tooltip_key, tooltip_key)
    folium.Circle(coords, radius=radius, color=color, weight=weight, fill=fill, fill_color=fill_color,
                  fill_opacity=fill_opacity, tooltip=tooltip_text).add_to(group)


train_pts = [(45.4642, 9.1900), (45.0703, 7.6869)]
bike1_pts = [(45.0703, 7.6869), (45.1885, 5.7245)]
bus_pts = [(45.1885, 5.7245), (43.3183, -1.9812)]
iberia_start_coord = (43.3183, -1.9812)
iberia_coords = [iberia_start_coord, (42.8800, -9.3000), (41.1500, -8.6300), (39.5000, -9.1300),
                 (38.7200, -9.1400), (37.0200, -8.9300), (37.0179, -7.9307)]
iberia_names_keys = ["map_sanseb_bike_popup", "map_finisterre_name", "map_porto_name", "map_ericeira_name", "map_lisbon_name", "map_sagres_name", "map_faro_name"]
iberia_dates_str = ["14 Set 25", "30 Sep 25", "10 Oct 25", "15 Oct 25", "20 Oct 25", "25 Oct 25", "28 Oct 25"]
faro_coord = (37.0179, -7.9307)
las_palmas_coord_simple = (28.1234, -15.4362)
sail_to_canaries_pts = [faro_coord, las_palmas_coord_simple]
st_lucia_coord_simple = (14.0108, -60.9707)
arc_pts = [las_palmas_coord_simple, st_lucia_coord_simple]
panama_canal_entry_approx = st_lucia_coord_simple  # Usato come punto di partenza per il segmento successivo
panama_city_coord = (9.0000, -79.5000)
sea_to_panama_pts = [panama_canal_entry_approx, panama_city_coord]
cross_pacific_coords = [panama_city_coord, (-0.9000, -89.6000), (-9.8000, -139.0000), (-17.5500, -149.5600)]
cross_pacific_names_keys = ["map_panama_pacific_start_popup", "map_galapagos_name", "map_marquesas_name", "map_tahiti_name"]
cross_pacific_arrival_dates_str = ["N/A", "10 Mar 26", "30 Apr 26", "15 Jun 26"]  # N/A per il punto di partenza
ecuador_coast_approx = (-2.1700, -79.9000)  # Guayaquil approx
sea_to_ecuador_pts = [st_lucia_coord_simple, ecuador_coast_approx]
bike_southam_coords = [ecuador_coast_approx, (-1.8300, -80.7500), (-4.4400, -81.2800), (-12.0500, -77.0400),
                       (-20.2300, -70.1400), (-34.3800, -72.0000)]
bike_southam_names_keys = ["map_guayaquil_bike_popup", "map_montanita_name", "map_lobitos_name", "map_lima_name", "map_iquique_name", "map_pichilemu_name"]
bike_southam_dates_str = ["01 Mar 26", "15 Apr 26", "15 May 26", "15 Jun 26", "01 Jul 26", "30 Jul 26"]


# --- 2. Generazione Mappa Folium (OTTIMIZZAZIONI POSSIBILI) ---
def generate_map_for_language(lang):
    current_texts = text_content[lang]

    # Inizializzazione mappa: location e zoom_start sono importanti.
    # Se la mappa è troppo zoomata all'inizio, potrebbe caricare più tile.
    # Un valore di zoom_start più basso (es. 2 o 3) mostra un'area più ampia.
    m = folium.Map(location=[20, -15], zoom_start=2, tiles=None)  # Meno zoom, centro più generico

    # Aggiungi i TileLayer. L'ordine influenza quello predefinito.
    folium.TileLayer('CartoDB positron', name=current_texts.get('map_tile_clear', "Clear Map"), attr="CartoDB Positron").add_to(m)
    folium.TileLayer('OpenStreetMap', name=current_texts.get('map_tile_standard', "Standard Map"), attr="OpenStreetMap").add_to(m)
    folium.TileLayer('Esri.WorldImagery', name=current_texts.get('map_tile_satellite', "Satellite Map"), attr="Esri World Imagery").add_to(m)

    main_fg = folium.FeatureGroup(name=current_texts['map_main_group'], show=True).add_to(m)
    planA_fg = folium.FeatureGroup(name=current_texts['map_planA_group'], show=False).add_to(m)
    planB_fg = folium.FeatureGroup(name=current_texts['map_planB_group'], show=False).add_to(m)

    # Percorso Principale
    add_marker_custom(45.4642, 9.1900, 'map_milan_popup', 'map_milan_date', "train", "#E74C3C", main_fg, current_texts)
    add_marker_custom(45.0703, 7.6869, 'map_turin_popup', 'map_turin_date', "train", "#E74C3C", main_fg, current_texts)
    add_line_custom(train_pts, "#E74C3C", "2,6", 'map_train_tooltip', main_fg, current_texts)

    add_marker_custom(45.0703, 7.6869, 'map_turin_bike_popup', 'map_turin_date', "person-biking", "#F39C12", main_fg, current_texts)  # Inizio bici Torino
    add_marker_custom(45.1885, 5.7245, 'map_grenoble_popup', 'map_grenoble_date', "person-biking", "#F39C12", main_fg, current_texts)  # Fine bici Grenoble
    add_line_custom(bike1_pts, "#F39C12", "5,8", 'map_bike1_tooltip', main_fg, current_texts)

    add_marker_custom(45.1885, 5.7245, 'map_grenoble_bus_popup', 'map_grenoble_bus_date', "bus", "#8E44AD", main_fg, current_texts)  # Bus da Grenoble
    add_marker_custom(iberia_start_coord[0], iberia_start_coord[1], 'map_sanseb_bus_popup', 'map_sanseb_bus_date', "bus", "#8E44AD", main_fg, current_texts)  # Arrivo bus San Seb
    add_line_custom(bus_pts, "#8E44AD", "2,10", 'map_bus_tooltip', main_fg, current_texts)

    for i, coord in enumerate(iberia_coords):  # Bici Iberica
        add_marker_custom(coord[0], coord[1], iberia_names_keys[i], iberia_dates_str[i], "person-biking", "#F39C12", main_fg, current_texts)
    add_line_custom(iberia_coords, "#F39C12", "5,8", 'map_iberia_bike_tooltip', main_fg, current_texts)

    add_marker_custom(faro_coord[0], faro_coord[1], 'map_faro_sail_popup', "29 Oct 25", "sailboat", "#2980B9", main_fg, current_texts)  # Partenza vela Faro
    add_marker_custom(las_palmas_coord_simple[0], las_palmas_coord_simple[1], 'map_las_palmas_popup', "23 Nov 25", "sailboat", "#2980B9", main_fg, current_texts)  # Arrivo Las Palmas
    add_line_custom(sail_to_canaries_pts, "#2980B9", "", 'map_sail_canaries_tooltip', main_fg, current_texts)
    add_circle_custom(las_palmas_coord_simple, 250000, "#2980B9", 1, True, "#AED6F1", 0.3, 'map_canaries_stop_tooltip', main_fg, current_texts)  # Sosta Canarie

    add_marker_custom(st_lucia_coord_simple[0], st_lucia_coord_simple[1], 'map_st_lucia_popup', "10-15 Dec 25", "sailboat", "#1A5276", main_fg, current_texts)  # Arrivo St. Lucia (ARC)
    add_line_custom(arc_pts, "#1A5276", "", 'map_arc_tooltip', main_fg, current_texts)  # Traversata ARC
    add_circle_custom(st_lucia_coord_simple, 300000, "#1A5276", 1, True, "#A9CCE3", 0.3, 'map_caribbean_explore_tooltip', main_fg, current_texts)  # Esplorazione Caraibi

    # Piano A: Traversata Pacifico
    add_marker_custom(panama_city_coord[0], panama_city_coord[1], 'map_panama_transfer_popup', "16 Feb 26", "anchor", "#5DADE2", planA_fg, current_texts)
    add_line_custom(sea_to_panama_pts, "#5DADE2", "4,8", 'map_sea_transfer_panama_tooltip', planA_fg, current_texts)
    add_circle_custom(panama_city_coord, 200000, "#8E44AD", 1, True, "#D5B9F8", 0.3, 'map_panama_prep_tooltip', planA_fg, current_texts)

    # Logica per Pacifico (Piano A) - Creazione dinamica tooltip
    current_point_A = cross_pacific_coords[0]  # Panama City
    add_marker_custom(current_point_A[0], current_point_A[1], cross_pacific_names_keys[0], "01 Mar 26", "sailboat", "#27AE60", planA_fg, current_texts)  # Partenza Panama
    prev_arrival_A_obj = datetime.strptime("01 Mar 26", "%d %b %y")

    for i in range(1, len(cross_pacific_coords)):
        next_pt_A = cross_pacific_coords[i]
        stop_name_key_A = cross_pacific_names_keys[i]
        arrival_dt_str_A = cross_pacific_arrival_dates_str[i]

        add_marker_custom(next_pt_A[0], next_pt_A[1], stop_name_key_A, arrival_dt_str_A, "sailboat", "#27AE60", planA_fg, current_texts)

        arrival_dt_obj_A = datetime.strptime(arrival_dt_str_A, "%d %b %y")

        from_loc_A_key = cross_pacific_names_keys[i - 1]
        from_loc_A_translated = current_texts.get(from_loc_A_key, from_loc_A_key.split('_')[1].capitalize())  # Heuristic for name
        to_loc_A_translated = current_texts.get(stop_name_key_A, stop_name_key_A.split('_')[1].capitalize())

        tooltip_sail_A = (f"{current_texts.get('map_sail_leg_tooltip_prefix', 'Sail')} "
                          f"{from_loc_A_translated}→{to_loc_A_translated} "
                          f"({prev_arrival_A_obj.strftime('%d %b %y')} - {arrival_dt_obj_A.strftime('%d %b %y')})")
        folium.PolyLine(locations=[current_point_A, next_pt_A], color="#27AE60", weight=4, dash_array="", tooltip=tooltip_sail_A).add_to(planA_fg)

        stay_end_A_obj = arrival_dt_obj_A + timedelta(days=15)  # Sosta di 15 giorni (esempio)
        tooltip_stop_A = (f"{current_texts.get('map_stopover_tooltip_prefix', 'Stopover at')} {to_loc_A_translated}\n"
                          f"{arrival_dt_obj_A.strftime('%d %b %y')} - {stay_end_A_obj.strftime('%d %b %y')}")
        folium.Circle(next_pt_A, radius=150000, color="#2ECC71", weight=1, fill=True, fill_color="#A9DFBF", fill_opacity=0.3, tooltip=tooltip_stop_A).add_to(planA_fg)

        current_point_A = next_pt_A
        prev_arrival_A_obj = stay_end_A_obj  # La prossima tappa parte dopo la sosta

    # Piano B: Bici Sudamerica
    add_marker_custom(ecuador_coast_approx[0], ecuador_coast_approx[1], 'map_ecuador_transfer_popup', "16 Feb 26", "anchor", "#5DADE2", planB_fg, current_texts)
    add_line_custom(sea_to_ecuador_pts, "#5DADE2", "4,8", 'map_sea_transfer_ecuador_tooltip', planB_fg, current_texts)
    add_circle_custom(ecuador_coast_approx, 200000, "#D35400", 1, True, "#EB984E", 0.3, 'map_ecuador_explore_tooltip', planB_fg, current_texts)

    for i, coord_B in enumerate(bike_southam_coords):
        add_marker_custom(coord_B[0], coord_B[1], bike_southam_names_keys[i], bike_southam_dates_str[i], "person-biking", "#E67E22", planB_fg, current_texts)
    add_line_custom(bike_southam_coords, "#E67E22", "5,8", 'map_bike_pacific_tooltip', planB_fg, current_texts)

    # Plugin (aggiunti per ultimi)
    plugins.Fullscreen(title=current_texts.get('map_fullscreen_title', "Fullscreen"), title_cancel=current_texts.get('map_fullscreen_cancel', "Exit Fullscreen")).add_to(m)
    plugins.MiniMap(tile_layer="CartoDB positron", toggle_display=True, minimized=True, zoomLevelOffset=-6).add_to(m)  # Minimappa usa tile leggeri
    plugins.LocateControl(strings={"title": current_texts.get('map_locate_title', "Show my location"), "popup": current_texts.get('map_locate_popup', "You are here (approx.)")}).add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)  # Layer control

    return m._repr_html_()


# --- Generazione dei file HTML ---
for lang_code in ['it', 'en']:
    lang_specific_texts = text_content[lang_code].copy()

    # URL specifici per lingua
    if lang_code == 'it':
        lang_specific_texts['brand_link_url'] = "index.html"  # Link del brand nella navbar
        lang_specific_texts['it_page_url'] = "index.html"
        lang_specific_texts['en_page_url'] = "en/index.html"
    else:  # lang_code == 'en'
        lang_specific_texts['brand_link_url'] = "index.html"  # Link del brand nella navbar
        lang_specific_texts['it_page_url'] = "../index.html"
        lang_specific_texts['en_page_url'] = "index.html"

    map_html = generate_map_for_language(lang_code)
    html_template = Template(HTML_TEMPLATE_STR)

    # Contesto per il rendering del template
    render_context = {**lang_specific_texts}  # Espande tutti i testi specifici per lingua
    render_context['map_html_fragment'] = map_html

    # URL delle immagini (relativi alla posizione del file HTML)
    # Se le immagini sono in /images/ e index.html è nella root, e en/index.html è in /en/
    if lang_code == 'it':
        img_prefix = "images/"
    else:  # en
        img_prefix = "../images/"  # Le immagini sono una cartella sopra rispetto a en/index.html

    render_context['gg_photo_url'] = img_prefix + "gg1.jpeg"
    render_context['paco_photo_url'] = img_prefix + "paco.jpeg"
    render_context['surf_photo_url'] = "https://www.thejambo.it/wp-content/uploads/2023/05/Le-migliori-destinazioni-al-mondo-per-fare-surf-Foto-di-Canva-3-1024x683.png"  # URL Esterno
    render_context['bike_setup_photo_url'] = img_prefix + "surfpacking1.jpg"
    render_context['grizl_photo_url'] = img_prefix + "grizl.jpg"
    render_context['ocean_crossing_photo_url'] = img_prefix + "ocean_crossing.jpg"

    rendered_html_content = html_template.render(render_context)

    # Percorso di output
    if lang_code == 'it':
        output_filename = "index.html"
        output_path = os.path.join(base_output_dir, output_filename)
    else:  # en
        output_filename = "index.html"
        output_path = os.path.join(base_output_dir, "en", output_filename)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rendered_html_content)
    print(f"Pagina in {lang_code.upper()} salvata in: {output_path}")

print("\n--- Processo di generazione completato con CSS ottimizzato per la mappa e JS per inizializzazione più rapida. ---")
print("Verifica la velocità di caricamento e la visualizzazione della mappa.")