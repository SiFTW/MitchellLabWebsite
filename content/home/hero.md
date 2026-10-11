+++
# Hero widget.
widget = "hero"
headless = true
active = true
weight = 1

title = "Systems Biology for Precision Oncology"

# Hero image (optional)
hero_media = "2023Photo.png"

[design.background]
  image_darken = 0.5
  text_color_light = true

[cta]
  url = "#projects"
  label = "Explore Our Research"
  icon_pack = "fas"
  icon = "flask"

[cta_alt]
  url = "#people"
  label = "Meet the Team"
  icon_pack = "fas"
  icon = "users"
+++

<!-- Full-bleed background video injected directly -->
<div style="position: absolute; top: 0; left: 0; width: 100vw; height: 100%; margin-left: calc(-50vw + 50%); pointer-events: none; overflow: hidden; z-index: 0;">
  <video autoplay loop muted playsinline poster="/media/genericBackgroundLarge.jpg" style="position: absolute; top: 50%; left: 50%; min-width: 100%; min-height: 100%; width: auto; height: auto; transform: translate(-50%, -50%); object-fit: cover;">
    <source src="/media/featured.mp4" type="video/mp4">
  </video>
  <div style="position: absolute; top: 0; left: 0; width: 100%; height: 100%; background: rgba(15, 23, 42, 0.7); z-index: 1;"></div>
</div>

<p style="font-size: 1.25rem; line-height: 1.6; color: #f8fafc; margin: 1.2rem 0 2rem 0; position: relative; z-index: 2; text-shadow: 0 2px 6px rgba(0,0,0,0.6);">
Bridging mechanistic mathematical modeling and wet-lab biology to tailor cancer therapies at Brighton and Sussex Medical School.
</p>
