---
# An instance of the Contact widget.
widget: contact

# This file represents a page section.
headless: true

# Order that this section appears on the page.
weight: 130

title: Contact
subtitle:

content:
  # Automatically link email and phone or display as text?
  autolink: true

  # Email form provider
  form:
    provider: netlify
    formspree:
      id:
    netlify:
      # Enable CAPTCHA challenge to reduce spam?
      captcha: false

  # Contact details (edit or remove options as required)
  email: S.A.Mitchell@bsms.ac.uk
  phone: 
  address:
    street: Medical Research Building, University of Sussex
    city: Falmer
    region: East Sussex
    postcode: 'BN1 9PX'
    country: United Kingdom
    country_code: UK
  coordinates:
    latitude: '50.864028'
    longitude: '-0.084734'
  directions: Enter the Medical Research Building (note this is behind the Medical Teaching Building) and call reception. We are on the second floor, up the stairs through the security door.
  office_hours:
  appointment_url: ''
  contact_links:
    - icon: twitter
      icon_pack: fab
      name: Twitter
      link: 'https://twitter.com/SiFTW'
    - icon: university
      icon_pack: fas
      name: Institution Website
      link: 'https://www.bsms.ac.uk/about/contact-us/staff/dr-simon-mitchell.aspx'
    - icon: phone
      icon_pack: fas
      name: '+44 (0)1273 678584'
      link: 'tel:+441273678584'
    - icon: orcid
      icon_pack: ai
      name: ORCID iD
      link: 'https://orcid.org/0000-0003-1091-6349'
    - icon: comments
      icon_pack: fas
      name: Book a Meeting with Simon
      link: 'https://calendly.com/simon_mitchell/chat-with-simon'
    - icon: google-scholar
      icon_pack: ai
      name: Google Scholar
      link: 'https://scholar.google.com/citations?user=lsKnTVoAAAAJ&hl=en'

design:
  columns: '2'
---
