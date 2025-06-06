# map_generator.py
import folium
from folium import plugins
from folium.features import DivIcon
from datetime import datetime, timedelta


def add_label(lat, lon, text, group):
    text_width = 150  # Puoi aggiustare questo valore
    folium.Marker(
        [lat, lon],
        icon=DivIcon(
            icon_size=(text_width, 24),  # Aumentato per un po' più di spazio se necessario
            icon_anchor=(text_width // 2, -10),  # Centrato, sopra il punto
            html=f'<div style="font-size:8pt; color:rgba(0,0,0,0.7); text-align:center; white-space: nowrap; width: {text_width}px; overflow: hidden; text-overflow: ellipsis;">{text}</div>'
        )
    ).add_to(group)


def add_marker_custom(lat, lon, name_key, date_key_or_str, icon, color, group, lang_texts):
    popup_name = lang_texts.get(name_key, name_key)  # Usa la chiave direttamente se non tradotta
    ico = plugins.BeautifyIcon(
        icon=icon, icon_shape='marker', background_color=color,
        border_color=color, text_color='white', prefix='fa'
    )
    folium.Marker([lat, lon], popup=popup_name, icon=ico).add_to(group)

    if date_key_or_str:
        # Se la data è una stringa con spazi (es. "10 Set 25"), usala direttamente.
        # Altrimenti, se è una chiave per lang_texts, traducila.
        date_text = date_key_or_str if ' ' in date_key_or_str or '/' in date_key_or_str or '-' in date_key_or_str and any(c.isalpha() for c in date_key_or_str) else lang_texts.get(date_key_or_str,
                                                                                                                                                                                    date_key_or_str)
        add_label(lat, lon, date_text, group)


def add_line_custom(points, color, dash, tooltip_key, group, lang_texts):
    tooltip_text = lang_texts.get(tooltip_key, tooltip_key)
    folium.PolyLine(points, color=color, weight=4, dash_array=dash, tooltip=tooltip_text).add_to(group)


def add_circle_custom(coords, radius, color, weight, fill, fill_color, fill_opacity, tooltip_key, group, lang_texts):
    tooltip_text = lang_texts.get(tooltip_key, tooltip_key)
    folium.Circle(coords, radius=radius, color=color, weight=weight, fill=fill, fill_color=fill_color,
                  fill_opacity=fill_opacity, tooltip=tooltip_text).add_to(group)


def generate_map_for_language(lang_code, current_texts, map_data_coords):
    """
    Genera la mappa Folium.
    map_data_coords è un dizionario che contiene tutte le coordinate e i nomi dei punti,
    prelevati da config.MAP_DATA_COORDS.
    """
    m = folium.Map(location=[20, -15], zoom_start=2, tiles=None)

    folium.TileLayer('CartoDB positron', name=current_texts.get('map_tile_clear', "Clear Map"), attr="CartoDB Positron").add_to(m)
    folium.TileLayer('OpenStreetMap', name=current_texts.get('map_tile_standard', "Standard Map"), attr="OpenStreetMap").add_to(m)
    folium.TileLayer('Esri.WorldImagery', name=current_texts.get('map_tile_satellite', "Satellite Map"), attr="Esri World Imagery").add_to(m)

    main_fg = folium.FeatureGroup(name=current_texts['map_main_group'], show=True).add_to(m)
    planA_fg = folium.FeatureGroup(name=current_texts['map_planA_group'], show=False).add_to(m)
    planB_fg = folium.FeatureGroup(name=current_texts['map_planB_group'], show=False).add_to(m)

    # Estrarre dati da map_data_coords per leggibilità
    train_pts = map_data_coords['train_pts']
    bike1_pts = map_data_coords['bike1_pts']
    bus_pts = map_data_coords['bus_pts']
    iberia_start_coord = map_data_coords['iberia_start_coord']
    iberia_coords = map_data_coords['iberia_coords']
    iberia_names_keys = map_data_coords['iberia_names_keys']
    iberia_dates_str = map_data_coords['iberia_dates_str']
    faro_coord = map_data_coords['faro_coord']
    las_palmas_coord = map_data_coords['las_palmas_coord_simple']
    sail_to_canaries_pts = map_data_coords['sail_to_canaries_pts']
    st_lucia_coord = map_data_coords['st_lucia_coord_simple']
    arc_pts = map_data_coords['arc_pts']
    panama_city_coord = map_data_coords['panama_city_coord']
    sea_to_panama_pts = map_data_coords['sea_to_panama_pts']
    cross_pacific_coords = map_data_coords['cross_pacific_coords']
    cross_pacific_names_keys = map_data_coords['cross_pacific_names_keys']
    cross_pacific_dates_str = map_data_coords['cross_pacific_arrival_dates_str']
    ecuador_coast_approx = map_data_coords['ecuador_coast_approx']
    sea_to_ecuador_pts = map_data_coords['sea_to_ecuador_pts']
    bike_southam_coords = map_data_coords['bike_southam_coords']
    bike_southam_names_keys = map_data_coords['bike_southam_names_keys']
    bike_southam_dates_str = map_data_coords['bike_southam_dates_str']

    # Percorso Principale
    add_marker_custom(train_pts[0][0], train_pts[0][1], 'map_milan_popup', 'map_milan_date', "train", "#E74C3C", main_fg, current_texts)
    add_marker_custom(train_pts[1][0], train_pts[1][1], 'map_turin_popup', 'map_turin_date', "train", "#E74C3C", main_fg, current_texts)
    add_line_custom(train_pts, "#E74C3C", "2,6", 'map_train_tooltip', main_fg, current_texts)

    add_marker_custom(bike1_pts[0][0], bike1_pts[0][1], 'map_turin_bike_popup', 'map_turin_date', "person-biking", "#F39C12", main_fg, current_texts)
    add_marker_custom(bike1_pts[1][0], bike1_pts[1][1], 'map_grenoble_popup', 'map_grenoble_date', "person-biking", "#F39C12", main_fg, current_texts)
    add_line_custom(bike1_pts, "#F39C12", "5,8", 'map_bike1_tooltip', main_fg, current_texts)

    add_marker_custom(bus_pts[0][0], bus_pts[0][1], 'map_grenoble_bus_popup', 'map_grenoble_bus_date', "bus", "#8E44AD", main_fg, current_texts)
    add_marker_custom(bus_pts[1][0], bus_pts[1][1], 'map_sanseb_bus_popup', 'map_sanseb_bus_date', "bus", "#8E44AD", main_fg, current_texts)
    add_line_custom(bus_pts, "#8E44AD", "2,10", 'map_bus_tooltip', main_fg, current_texts)

    for i, coord in enumerate(iberia_coords):
        add_marker_custom(coord[0], coord[1], iberia_names_keys[i], iberia_dates_str[i], "person-biking", "#F39C12", main_fg, current_texts)
    add_line_custom(iberia_coords, "#F39C12", "5,8", 'map_iberia_bike_tooltip', main_fg, current_texts)

    add_marker_custom(faro_coord[0], faro_coord[1], 'map_faro_sail_popup', "29 Oct 25", "sailboat", "#2980B9", main_fg, current_texts)
    add_marker_custom(las_palmas_coord[0], las_palmas_coord[1], 'map_las_palmas_popup', "23 Nov 25", "sailboat", "#2980B9", main_fg, current_texts)
    add_line_custom(sail_to_canaries_pts, "#2980B9", "", 'map_sail_canaries_tooltip', main_fg, current_texts)
    add_circle_custom(las_palmas_coord, 250000, "#2980B9", 1, True, "#AED6F1", 0.3, 'map_canaries_stop_tooltip', main_fg, current_texts)

    add_marker_custom(st_lucia_coord[0], st_lucia_coord[1], 'map_st_lucia_popup', "10-15 Dic 25", "sailboat", "#1A5276", main_fg, current_texts)
    add_line_custom(arc_pts, "#1A5276", "", 'map_arc_tooltip', main_fg, current_texts)
    add_circle_custom(st_lucia_coord, 300000, "#1A5276", 1, True, "#A9CCE3", 0.3, 'map_caribbean_explore_tooltip', main_fg, current_texts)

    # Piano A: Traversata Pacifico
    add_marker_custom(panama_city_coord[0], panama_city_coord[1], 'map_panama_transfer_popup', "16 Feb 26", "anchor", "#5DADE2", planA_fg, current_texts)
    add_line_custom(sea_to_panama_pts, "#5DADE2", "4,8", 'map_sea_transfer_panama_tooltip', planA_fg, current_texts)
    add_circle_custom(panama_city_coord, 200000, "#8E44AD", 1, True, "#D5B9F8", 0.3, 'map_panama_prep_tooltip', planA_fg, current_texts)

    current_point_A = cross_pacific_coords[0]
    add_marker_custom(current_point_A[0], current_point_A[1], cross_pacific_names_keys[0], "01 Mar 26", "sailboat", "#27AE60", planA_fg, current_texts)
    prev_arrival_A_obj = datetime.strptime("01 Mar 26", "%d %b %y")

    for i in range(1, len(cross_pacific_coords)):
        next_pt_A = cross_pacific_coords[i]
        stop_name_key_A = cross_pacific_names_keys[i]
        arrival_dt_str_A = cross_pacific_dates_str[i]

        add_marker_custom(next_pt_A[0], next_pt_A[1], stop_name_key_A, arrival_dt_str_A, "sailboat", "#27AE60", planA_fg, current_texts)
        arrival_dt_obj_A = datetime.strptime(arrival_dt_str_A, "%d %b %y")

        from_loc_A_key = cross_pacific_names_keys[i - 1]  # Chiave del nome precedente
        from_loc_A_translated = current_texts.get(from_loc_A_key, from_loc_A_key.replace("map_", "").replace("_popup", "").replace("_name", "").replace("_pacific_start", "").capitalize())
        to_loc_A_translated = current_texts.get(stop_name_key_A, stop_name_key_A.replace("map_", "").replace("_name", "").capitalize())

        tooltip_sail_A = (f"{current_texts.get('map_sail_leg_tooltip_prefix', 'Sail')} "
                          f"{from_loc_A_translated}→{to_loc_A_translated} "
                          f"({prev_arrival_A_obj.strftime('%d %b %y')} - {arrival_dt_obj_A.strftime('%d %b %y')})")
        folium.PolyLine(locations=[current_point_A, next_pt_A], color="#27AE60", weight=4, dash_array="", tooltip=tooltip_sail_A).add_to(planA_fg)

        stay_end_A_obj = arrival_dt_obj_A + timedelta(days=15)
        tooltip_stop_A = (f"{current_texts.get('map_stopover_tooltip_prefix', 'Stopover at')} {to_loc_A_translated}\n"
                          f"{arrival_dt_obj_A.strftime('%d %b %y')} - {stay_end_A_obj.strftime('%d %b %y')}")
        folium.Circle(next_pt_A, radius=150000, color="#2ECC71", weight=1, fill=True, fill_color="#A9DFBF", fill_opacity=0.3, tooltip=tooltip_stop_A).add_to(planA_fg)

        current_point_A = next_pt_A
        prev_arrival_A_obj = stay_end_A_obj

    # Piano B: Bici Sudamerica
    add_marker_custom(ecuador_coast_approx[0], ecuador_coast_approx[1], 'map_ecuador_transfer_popup', "16 Feb 26", "anchor", "#5DADE2", planB_fg, current_texts)
    add_line_custom(sea_to_ecuador_pts, "#5DADE2", "4,8", 'map_sea_transfer_ecuador_tooltip', planB_fg, current_texts)
    add_circle_custom(ecuador_coast_approx, 200000, "#D35400", 1, True, "#EB984E", 0.3, 'map_ecuador_explore_tooltip', planB_fg, current_texts)

    for i, coord_B in enumerate(bike_southam_coords):
        add_marker_custom(coord_B[0], coord_B[1], bike_southam_names_keys[i], bike_southam_dates_str[i], "person-biking", "#E67E22", planB_fg, current_texts)
    add_line_custom(bike_southam_coords, "#E67E22", "5,8", 'map_bike_pacific_tooltip', planB_fg, current_texts)

    plugins.Fullscreen(title=current_texts.get('map_fullscreen_title', "Fullscreen"), title_cancel=current_texts.get('map_fullscreen_cancel', "Exit Fullscreen")).add_to(m)
    plugins.MiniMap(tile_layer="CartoDB positron", toggle_display=True, minimized=True, zoomLevelOffset=-6).add_to(m)
    plugins.LocateControl(strings={"title": current_texts.get('map_locate_title', "Show my location"), "popup": current_texts.get('map_locate_popup', "You are here (approx.)")}).add_to(m)

    folium.LayerControl(collapsed=False).add_to(m)
    return m._repr_html_()