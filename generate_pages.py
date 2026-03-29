#!/usr/bin/env python3
"""Generate all HTML pages for balitrip-site with external CSS/JS."""

import json
import os
import urllib.parse

SITE_DIR = "/home/ubuntu/balitrip-site/site"
DATA_FILE = "/home/ubuntu/scrape_tour_pages.json"

WA_NUM = "6285935490002"
WA_SVG = '<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 2.898a9.825 9.825 0 012.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>'

# Image map from balitrip.ru cards
CARD_IMAGES = {
    "Убут и окрестности деревни": "https://i.siteapi.org/0X82NETv_2flGqskafB7v_kKjJ8=/fit-in/256x256/filters:fill(transparent):format(png)/8e6d329dd9d1493.s2.siteapi.org/page/1dam3n48ne804kgco44cwwk4k88gck",
    "Приключенческий тур": "https://i.siteapi.org/xY9gq7OElgACKHT8dUDQoUDwbsg=/fit-in/256x256/filters:fill(transparent):format(png)/8e6d329dd9d1493.s2.siteapi.org/page/n4wscjpfkhwkcwgsgosso8kk8k4owg",
    "Тур к вулкану без подъема 1": "https://i.siteapi.org/JpU-E3sUPIwe7MFptQsys8l1luY=/fit-in/256x256/filters:fill(transparent):format(png)/8e6d329dd9d1493.s2.siteapi.org/page/sdk3b93rxkgos0sww40wo40g4co80g",
    "Тур к вулкану без подъема 2": "https://i.siteapi.org/gVkgOWzgqKFkgTK0hRLPpxJEXR8=/fit-in/256x256/filters:fill(transparent):format(png)/8e6d329dd9d1493.s2.siteapi.org/page/k6ju6zc360goowgwkc8kgosgoo44gc",
    "Тур к вулкану без подъема 3": "https://i.siteapi.org/bA7gIGE7l6H5o1s52yFy3SrFYhA=/fit-in/256x256/filters:fill(transparent):format(png)/8e6d329dd9d1493.s2.siteapi.org/page/4c8qyjl96zs48wgsgsg8cwc48w84s8",
    "Тур на северо-запад острова 1": "https://i.siteapi.org/zbOyitasd242wLyDA-Xj0AnqSBs=/fit-in/256x256/filters:fill(transparent):format(png)/8e6d329dd9d1493.s2.siteapi.org/page/kupvmq6jb808ko88kkkowo8g88440c",
    "Тур на северо-запад острова 2": "https://i.siteapi.org/E0qNB8q9GZ_CUsvyEFf3cXJqkKQ=/fit-in/256x256/filters:fill(transparent):format(png)/8e6d329dd9d1493.s2.siteapi.org/page/2bkqfhgxdvk8cg0o4g0cckw0o4oo0g",
    "Тур на восток острова 1": "https://i.siteapi.org/tRCE1U_exZtli6DZFrHUhIqFKZo=/fit-in/256x256/filters:fill(transparent):format(png)/8e6d329dd9d1493.s2.siteapi.org/page/rj5ufqxqhkw0k0wk0s4g0kwg4w4ggg",
    "Тур на восток острова 2": "https://i.siteapi.org/vxTO0cbS-R5ubNkIoMlrVXPjqXY=/fit-in/256x256/filters:fill(transparent):format(png)/8e6d329dd9d1493.s2.siteapi.org/page/3rl5zcqt0ys0kcw0k8csw4kkk0g8o0",
    "Тур по пляжам на Юге Бали": "https://i.siteapi.org/Xt0fxWdBxnKlYkr1Y0VvJIqAqKM=/fit-in/256x256/filters:fill(transparent):format(png)/8e6d329dd9d1493.s2.siteapi.org/page/3g3iqwqnfkw0s8s4kk0gk0kkc4g0ow",
    "Тур на север острова": "https://i.siteapi.org/Xqv1qfWBLPfFAyJ8GBvMmHCVjxE=/fit-in/256x256/filters:fill(transparent):format(png)/8e6d329dd9d1493.s2.siteapi.org/page/6vxgxvt1nh4ckk4s8g4w0ggkwg8w4o",
    "Восхождение по вулкану Батур": "https://i.siteapi.org/y8-D7EK1M3O5vK95nJqbVQ-YRSI=/fit-in/256x256/filters:fill(transparent):format(png)/8e6d329dd9d1493.s2.siteapi.org/page/1hqvj1dg1d6o4c4c0g8s0cks8ckwg0",
    "Тур на север Бали к дельфинам": "https://i.siteapi.org/6Gg4Xn3Vy5MHb2Zp1xUQPbkxLBg=/fit-in/256x256/filters:fill(transparent):format(png)/8e6d329dd9d1493.s2.siteapi.org/page/3rl5zcqt0ys0kcw0k8csw4kkk0g8o0",
    "Тур на север Бали с ночёвкой": "https://i.siteapi.org/Xqv1qfWBLPfFAyJ8GBvMmHCVjxE=/fit-in/256x256/filters:fill(transparent):format(png)/8e6d329dd9d1493.s2.siteapi.org/page/6vxgxvt1nh4ckk4s8g4w0ggkwg8w4o",
}

HERO_IMG = "https://i.siteapi.org/lZd-b20kuhq5VGsxJaTHyZIuLFg=/8e6d329dd9d1493.s2.siteapi.org/page/737qmp5nescgwc0os8gcc4s4wwo08g"
INDIVIDUAL_IMG = "https://i.siteapi.org/j7OZFM_6DeC1ymqIN7z5PM9VM4E=/8e6d329dd9d1493.s2.siteapi.org/page/mkutd4uyq5wccws0wg4ow4o404kcos"

SLUG_MAP = {
    "Убут и окрестности деревни": "ubut-i-okrestnosti-derevni",
    "Приключенческий тур": "priklyuchencheskiy-tur",
    "Тур к вулкану без подъема 1": "tur-k-vulkanu-bez-podema-1",
    "Тур к вулкану без подъема 2": "tur-k-vulkanu-bez-podema-2",
    "Тур к вулкану без подъема 3": "tur-k-vulkanu-bez-podema-3",
    "Тур на северо-запад острова 1": "tur-na-severo-zapad-ostrova-1",
    "Тур на северо-запад острова 2": "tur-na-severo-zapad-ostrova-2",
    "Тур на восток острова 1": "tur-na-vostok-ostrova",
    "Тур на восток острова 2": "tur-na-vostok-ostrova-2",
    "Тур по пляжам на Юге Бали": "tur-po-plyazham-na-yuge-bali",
    "Тур на север острова": "tur-na-sever-ostrova",
    "Восхождение по вулкану Батур": "voshozhdenie-po-vulkanu-batur",
    "Тур на север Бали к дельфинам": "tur-na-sever-bali-k-delfinam",
    "Тур на север Бали с ночёвкой": "tur-na-sever-bali-s-nochyovkoy",
}

def wa_link(text):
    return f"https://wa.me/{WA_NUM}?text={urllib.parse.quote(text)}"

def header_html(active="home"):
    active_home = ' class="active"' if active == "home" else ""
    active_tours = ' class="active"' if active == "tours" else ""
    return f"""  <header class="site-header">
    <div class="container header-inner">
      <a href="/" class="logo">Bali<span>Trip</span></a>
      <nav>
        <ul class="nav-links" id="navLinks">
          <li><a href="/"{active_home}>Главная</a></li>
          <li><a href="/tours.html"{active_tours}>Экскурсии</a></li>
          <li><a href="/#how-we-work">Как заказать</a></li>
          <li><a href="/#contact-form">Заявка на тур</a></li>
          <li><a href="https://wa.me/{WA_NUM}" class="nav-wa">WhatsApp</a></li>
          <li><a href="mailto:MADETINGKES@MAIL.RU">Email</a></li>
        </ul>
      </nav>
      <button class="menu-toggle" id="menuToggle" aria-label="Открыть меню">
        <span></span><span></span><span></span>
      </button>
    </div>
  </header>"""

def footer_html():
    return f"""  <footer class="site-footer">
    <div class="container footer-inner">
      <div class="footer-contacts">
        <a href="https://wa.me/{WA_NUM}" class="footer-wa">WhatsApp: +6285935490002</a>
        <a href="mailto:MADETINGKES@MAIL.RU">Email: MADETINGKES@MAIL.RU</a>
      </div>
      <p class="footer-disclaimer">Данный сайт носит информационно-справочный характер и не является публичной офертой.</p>
    </div>
  </footer>"""

def page_wrap(title, description, body, active="home"):
    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{description}">
  <link rel="stylesheet" href="/css/main.css">
  <link rel="stylesheet" href="/css/mobile.css">
</head>
<body>
{header_html(active)}
  <main>
{body}
  </main>
{footer_html()}
  <script src="/js/main.js"></script>
</body>
</html>
"""

def tour_card_html(title, desc, price, slug, img_url):
    short_desc = desc[:160] if desc else ""
    return f"""<article class="tour-card">
            <div class="tour-card-img">
              <img referrerpolicy="no-referrer" src="{img_url}" alt="{title}" loading="lazy">
            </div>
            <div class="tour-card-body">
              <h3>{title}</h3>
              <p class="tour-card-desc">{short_desc}</p>
              <div class="tour-card-footer">
                <div class="tour-card-price">{price} <small>/ чел</small></div>
                <a href="/{slug}.html" class="tour-card-link">Подробнее &rarr;</a>
              </div>
            </div>
          </article>"""


def generate_index(tours):
    # First 6 tours for homepage
    cards = ""
    for t in tours[:6]:
        title = t["title"]
        slug = SLUG_MAP.get(title, "")
        img = CARD_IMAGES.get(title, "")
        price = t.get("price", "")
        desc = t.get("description", "")
        cards += tour_card_html(title, desc, price, slug, img) + "\n"

    wa_general = wa_link("Здравствуйте! Интересуют экскурсии на Бали.")
    wa_individual = wa_link("Здравствуйте! Интересует тур: Индивидуальная экскурсия. Подскажите детали, пожалуйста.")

    body = f"""
    <!-- ===== HERO ===== -->
    <section class="hero">
      <img referrerpolicy="no-referrer" class="hero-img" src="{HERO_IMG}" alt="Экскурсии и туры на Бали">
      <div class="hero-overlay"></div>
      <div class="container hero-content">
        <h1>Эксклюзивные экскурсии и туры на Бали</h1>
        <p class="hero-subtitle">Отправляйтесь в незабываемое приключение по Бали в сопровождении русскоговорящего гида. Мы подарим Вам эмоции и незабываемые впечатления!</p>
        <div class="hero-chips">
          <span class="hero-chip">Русскоговорящие гиды</span>
          <span class="hero-chip">Доступные цены</span>
          <span class="hero-chip">Без посредников</span>
          <span class="hero-chip">Большой опыт</span>
        </div>
        <a class="btn-wa" href="{wa_general}">
          {WA_SVG}
          Написать в WhatsApp
        </a>
        <span class="btn-hint">Сообщение уже заполнено — просто нажмите</span>
      </div>
    </section>

    <!-- ===== TRUST ===== -->
    <section class="section trust">
      <div class="container">
        <h2 class="section-title">Что мы предлагаем?</h2>
        <p class="section-subtitle">Мы организуем индивидуальные и групповые экскурсии на Бали для русскоговорящих гостей.</p>
        <div class="trust-grid">
          <div class="trust-card"><div class="trust-icon">&#127759;</div><div><h3>Русскоговорящие гиды</h3><p>Всё общение на русском языке — никаких языковых барьеров</p></div></div>
          <div class="trust-card"><div class="trust-icon">&#127965;</div><div><h3>Разнообразные экскурсии</h3><p>14 готовых маршрутов и индивидуальные туры по вашим пожеланиям</p></div></div>
          <div class="trust-card"><div class="trust-icon">&#128176;</div><div><h3>Доступные цены</h3><p>Работаете напрямую с организатором — честная цена без переплат</p></div></div>
          <div class="trust-card"><div class="trust-icon">&#128172;</div><div><h3>Удобный способ связи</h3><p>Ответим в WhatsApp за минуты — уточните любые детали</p></div></div>
          <div class="trust-card"><div class="trust-icon">&#10084;&#65039;</div><div><h3>Большой опыт</h3><p>Знаем остров как свои пять пальцев — покажем лучшее</p></div></div>
          <div class="trust-card"><div class="trust-icon">&#128663;</div><div><h3>Комфорт</h3><p>Удобная машина, трансфер из отеля и обратно</p></div></div>
        </div>
      </div>
    </section>

    <!-- ===== TOURS PREVIEW ===== -->
    <section class="section" id="tours">
      <div class="container">
        <h2 class="section-title">Готовые экскурсии</h2>
        <p class="section-subtitle">Вы увидите много красивых популярных и уникальных, рукотворных и природных достопримечательностей острова.</p>
        <div class="tours-grid">
{cards}
        </div>
        <div class="all-tours-link">
          <a href="/tours.html" class="tour-card-link" style="padding:14px 32px;font-size:15px;">Все 14 экскурсий &rarr;</a>
        </div>
      </div>
    </section>

    <!-- ===== INDIVIDUAL TOUR ===== -->
    <section class="section individual-section">
      <div class="container">
        <div class="details-grid">
          <div class="individual-img">
            <img referrerpolicy="no-referrer" src="{INDIVIDUAL_IMG}" alt="Индивидуальная экскурсия на Бали">
          </div>
          <div class="details-text">
            <h2>Индивидуальная экскурсия</h2>
            <p>Предоставим машину с русскоговорящим водителем/гидом, который составит индивидуальную экскурсию специально по вашим пожеланиям.</p>
            <ul class="individual-list">
              <li><span class="individual-check">&#10003;</span> Фиксированная стоимость за день</li>
              <li><span class="individual-check">&#10003;</span> Русскоговорящий водитель/гид</li>
              <li><span class="individual-check">&#10003;</span> Удобная машина только для вас</li>
              <li><span class="individual-check">&#10003;</span> Никуда не торопим</li>
              <li><span class="individual-check">&#10003;</span> Трансфер из отеля и в отель</li>
            </ul>
            <a class="btn-wa" href="{wa_individual}">
              {WA_SVG}
              Обсудить маршрут
            </a>
            <span class="btn-hint btn-hint--dark">Напишите — составим маршрут под вас</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== HOW WE WORK ===== -->
    <section class="section how-we-work" id="how-we-work">
      <div class="container">
        <h2 class="section-title section-title--center">Как мы работаем?</h2>
        <p class="section-subtitle section-subtitle--center">Три простых шага до незабываемого путешествия</p>
        <div class="steps-grid">
          <div class="step-card">
            <div class="step-num">1</div>
            <h3>Свяжитесь с нами</h3>
            <p>Любым удобным способом — WhatsApp, email или форма на сайте</p>
          </div>
          <div class="step-card">
            <div class="step-num">2</div>
            <h3>Обговорим все условия</h3>
            <p>Договоримся о времени проведения тура и всех деталях</p>
          </div>
          <div class="step-card">
            <div class="step-num">3</div>
            <h3>Проведём незабываемый тур</h3>
            <p>Впечатления о котором останутся у вас навсегда</p>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== CONTACT FORM ===== -->
    <section class="form-section" id="contact-form">
      <div class="container">
        <div class="form-grid">
          <div class="form-info">
            <h2>Заполните форму</h2>
            <p>Хотите заказать экскурсию по о. Бали? Оставьте заявку и мы свяжемся с вами любым удобным для вас способом!</p>
          </div>
          <form class="contact-form" action="#" onsubmit="return false;">
            <input type="text" placeholder="Имя*" required>
            <input type="tel" placeholder="Телефон*" required>
            <input type="email" placeholder="E-mail">
            <textarea placeholder="Комментарий"></textarea>
            <label class="form-consent">
              <input type="checkbox" required>
              Я даю согласие на обработку персональных данных
            </label>
            <button type="submit" class="btn-submit">Отправить заявку</button>
          </form>
        </div>
      </div>
    </section>
"""
    return page_wrap(
        "BaliTrip — Экскурсии и туры на Бали",
        "Эксклюзивные экскурсии и туры на Бали с русскоговорящим гидом. 14 готовых маршрутов и индивидуальные туры. Бронируйте напрямую без посредников.",
        body,
        active="home"
    )


def generate_tours(tours):
    cards = ""
    for t in tours:
        title = t["title"]
        slug = SLUG_MAP.get(title, "")
        img = CARD_IMAGES.get(title, "")
        price = t.get("price", "")
        desc = t.get("description", "")
        cards += tour_card_html(title, desc, price, slug, img) + "\n"

    wa_individual = wa_link("Здравствуйте! Хочу обсудить индивидуальный маршрут по Бали.")

    body = f"""
    <!-- ===== HERO ===== -->
    <section class="hero hero--compact">
      <img referrerpolicy="no-referrer" class="hero-img" src="{HERO_IMG}" alt="Экскурсии на Бали">
      <div class="hero-overlay"></div>
      <div class="container hero-content">
        <h1>Экскурсии на Бали</h1>
        <p class="hero-subtitle">14 готовых маршрутов по самым красивым местам острова. Русскоговорящий гид, комфортная машина, честные цены.</p>
      </div>
    </section>

    <!-- ===== ALL TOURS ===== -->
    <section class="section">
      <div class="container">
        <div class="tours-grid">
{cards}
        </div>
      </div>
    </section>

    <!-- ===== CTA ===== -->
    <section class="cta-section">
      <h2>Не нашли подходящий тур?</h2>
      <p>Составим индивидуальный маршрут специально для вас — напишите в WhatsApp</p>
      <a class="btn-wa" href="{wa_individual}">
        {WA_SVG}
        Обсудить маршрут
      </a>
      <span class="btn-hint" style="color:rgba(255,255,255,.4);">Сообщение уже заполнено — просто нажмите</span>
    </section>

    <!-- ===== WHY US ===== -->
    <section class="section" style="background:#fff;">
      <div class="container">
        <h2 class="section-title section-title--center">Почему выбирают нас</h2>
        <p class="section-subtitle section-subtitle--center">Мы организуем экскурсии напрямую, без посредников и переплат</p>
        <div class="why-grid">
          <div class="why-card"><div class="why-icon">&#127759;</div><div><h3>Русскоговорящий гид</h3><p>Всё общение на русском языке</p></div></div>
          <div class="why-card"><div class="why-icon">&#9989;</div><div><h3>Без посредников</h3><p>Работаете напрямую с организатором</p></div></div>
          <div class="why-card"><div class="why-icon">&#128506;</div><div><h3>Понятный маршрут</h3><p>Заранее знаете, что вас ждёт</p></div></div>
          <div class="why-card"><div class="why-icon">&#128172;</div><div><h3>Быстрая связь</h3><p>Ответим в WhatsApp за минуты</p></div></div>
        </div>
      </div>
    </section>
"""
    return page_wrap(
        "Экскурсии на Бали — BaliTrip",
        "Все экскурсии на Бали: 14 готовых маршрутов с русскоговорящим гидом. Вулканы, водопады, храмы, пляжи. Бронируйте напрямую.",
        body,
        active="tours"
    )


def generate_tour_page(t):
    title = t["title"]
    slug = SLUG_MAP.get(title, "")
    desc = t.get("description", "")
    price = t.get("price", "")
    highlights = t.get("highlights", [])
    included = t.get("included", [])
    not_included = t.get("not_included", [])
    departure = t.get("departure_time", "")
    guide = t.get("guide", "Русскоговорящий")
    img = CARD_IMAGES.get(title, HERO_IMG)

    wa_text = wa_link(f"Здравствуйте! Интересует тур: {title}. Подскажите детали, пожалуйста.")

    # Highlights chips
    chips_html = ""
    for h in highlights:
        chips_html += f'          <span class="hero-chip">{h}</span>\n'

    # Included list
    inc_items = ""
    for item in included:
        inc_items += f'              <li>{item}</li>\n'

    not_inc_items = ""
    for item in not_included:
        not_inc_items += f'              <li>{item}</li>\n'

    # Sidebar
    sidebar_items = ""
    if departure:
        sidebar_items += f"""            <div class="sidebar-item">
              <span class="sidebar-label">Время выезда</span>
              <span class="sidebar-value">{departure}</span>
            </div>\n"""
    if price:
        sidebar_items += f"""            <div class="sidebar-item">
              <span class="sidebar-label">Цена</span>
              <span class="sidebar-value">{price}</span>
            </div>\n"""
    sidebar_items += f"""            <div class="sidebar-item">
              <span class="sidebar-label">Гид</span>
              <span class="sidebar-value">{guide}</span>
            </div>"""

    body = f"""
    <!-- ===== HERO ===== -->
    <section class="hero hero--compact">
      <img referrerpolicy="no-referrer" class="hero-img" src="{img}" alt="{title}">
      <div class="hero-overlay"></div>
      <div class="container hero-content">
        <div class="breadcrumbs">
          <a href="/">Главная</a><span>›</span><a href="/tours.html">Экскурсии</a><span>›</span>{title}
        </div>
        <h1>{title}</h1>
        <div class="hero-chips">
{chips_html}        </div>
        <a class="btn-wa" href="{wa_text}">
          {WA_SVG}
          Написать в WhatsApp
        </a>
        <span class="btn-hint">Сообщение уже заполнено — просто нажмите</span>
      </div>
    </section>

    <!-- ===== DETAILS ===== -->
    <section class="section details">
      <div class="container">
        <div class="details-grid">
          <div class="details-text">
            <h2>Описание маршрута</h2>
            <p>{desc}</p>
          </div>
          <div class="details-sidebar">
            <h3>Краткая информация</h3>
{sidebar_items}
            <a class="btn-wa" href="{wa_text}" style="margin-top:24px;width:100%;justify-content:center;">
              {WA_SVG}
              Забронировать
            </a>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== INCLUDED ===== -->
    <section class="section includes">
      <div class="container">
        <h2 class="section-title">Что входит в стоимость</h2>
        <div class="includes-grid">
          <div class="includes-card included">
            <h3>В стоимость входит</h3>
            <ul class="includes-list">
{inc_items}            </ul>
          </div>
          <div class="includes-card not-included">
            <h3>В стоимость не входит</h3>
            <ul class="includes-list">
{not_inc_items}            </ul>
          </div>
        </div>
      </div>
    </section>

    <!-- ===== CTA ===== -->
    <section class="cta-section">
      <h2>Готовы отправиться в путешествие?</h2>
      <p>Напишите нам в WhatsApp — ответим за минуты, подберём удобную дату и всё организуем</p>
      <a class="btn-wa" href="{wa_text}">
        {WA_SVG}
        Написать в WhatsApp
      </a>
      <span class="btn-hint" style="color:rgba(255,255,255,.4);">Сообщение уже заполнено — просто нажмите</span>
    </section>
"""
    return page_wrap(
        f"Туры на Бали - {title}",
        f"{title} — экскурсия на Бали с русскоговорящим гидом. {desc[:120]}",
        body,
        active="tours"
    )


def parse_data_file(filepath):
    """Parse the data_file to extract included/not_included."""
    included = []
    not_included = []
    departure = ""
    try:
        with open(filepath, 'r') as f:
            content = f.read()
        for line in content.split('\n'):
            if line.startswith('В стоимость тура входит:'):
                items = line.replace('В стоимость тура входит:', '').strip()
                included = [i.strip() for i in items.split(',') if i.strip()]
            elif line.startswith('В стоимость тура не входит:'):
                items = line.replace('В стоимость тура не входит:', '').strip()
                not_included = [i.strip() for i in items.split(',') if i.strip()]
            elif line.startswith('Время выезда:'):
                departure = line.replace('Время выезда:', '').strip()
    except:
        pass
    return included, not_included, departure


def normalize_tours(raw_data):
    """Convert raw scrape results to normalized tour dicts."""
    results = raw_data.get('results', [])
    tours = []
    for r in results:
        out = r.get('output', {})
        data_file = out.get('data_file', '')
        included, not_included, departure = parse_data_file(data_file)
        route_points = [p.strip() for p in out.get('route_points', '').split(';') if p.strip()]
        # Clean description: remove lines with price/time/included info
        raw_desc = out.get('full_description', '')
        clean_lines = []
        for line in raw_desc.split('\n'):
            line_stripped = line.strip()
            if any(line_stripped.startswith(prefix) for prefix in [
                'Время выезда:', 'Цена тура:', 'В стоимость тура входит:', 'В стоимость тура не входит:',
                'Цена:', 'Стоимость:'
            ]):
                continue
            clean_lines.append(line_stripped)
        cleaned_desc = ' '.join(clean_lines).strip()
        # Replace literal \n with actual line breaks for HTML
        cleaned_desc = cleaned_desc.replace('\\n', '<br>')
        t = {
            'title': out.get('tour_name', ''),
            'description': cleaned_desc,
            'price': out.get('price_info', ''),
            'highlights': route_points,
            'included': included or ['машина', 'бензин', 'водитель'],
            'not_included': not_included or ['входные билеты и питание'],
            'departure_time': departure,
            'guide': 'Русскоговорящий',
        }
        tours.append(t)
    return tours


def main():
    with open(DATA_FILE, "r") as f:
        raw_data = json.load(f)

    tours = normalize_tours(raw_data)
    os.makedirs(SITE_DIR, exist_ok=True)

    # Generate index.html
    with open(os.path.join(SITE_DIR, "index.html"), "w") as f:
        f.write(generate_index(tours))
    print("Generated: site/index.html")

    # Generate tours.html
    with open(os.path.join(SITE_DIR, "tours.html"), "w") as f:
        f.write(generate_tours(tours))
    print("Generated: site/tours.html")

    # Generate individual tour pages
    for t in tours:
        title = t["title"]
        slug = SLUG_MAP.get(title)
        if not slug:
            print(f"WARNING: No slug for '{title}', skipping")
            continue
        filepath = os.path.join(SITE_DIR, f"{slug}.html")
        with open(filepath, "w") as f:
            f.write(generate_tour_page(t))
        print(f"Generated: site/{slug}.html")

    print(f"\nDone! Generated {2 + len(tours)} pages total.")


if __name__ == "__main__":
    main()
