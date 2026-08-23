from playwright.sync_api import Page, expect

def test_homepage(page: Page):
  page.goto("http://127.0.0.1:8000")

  expect(page).to_have_title("Nutrifood")

def test_homepage_content(page: Page):
  page.goto("http://127.0.0.1:8000")

  expect(page.locator("h1")).to_have_text("Bienvenue sur Nutrifood")
  expect(page.get_by_label("Nom du produit")).to_be_empty()
  expect(page.get_by_role("link", name="Trouver une meilleure alternative")).to_have_attribute("href", "/alternative/")

def test_rechercher_produit(page: Page):
  page.goto("http://127.0.0.1:8000/")

  page.get_by_label("Nom du produit").fill("Coca-Cola")
  page.get_by_role("button", name="Rechercher").click()

  expect(page).to_have_url("http://127.0.0.1:8000/recherche/?q=Coca-Cola"
  )

  expect(page.locator("h1")).to_have_text('Résultats de la recherche pour "Coca-Cola" ')

  produits = page.locator(".produit-item")

  expect(produits).to_have_count(3)

  expect(produits.first).to_contain_text("Coca-Cola")

  expect(produits.first).to_contain_text("Nutriscore: E")

  expect(produits.first).to_contain_text("Catégorie: Boissons")

  expect(produits.first.get_by_role("link", name="Voir les détails")).to_have_attribute("href", "/1234567890123/")

def test_detail_produit(page: Page):
  page.goto("http://127.0.0.1:8000/")

  page.get_by_label("Nom du produit").fill("Coca-Cola")
  page.get_by_role("button", name="Rechercher").click()

  produit = page.locator(".produit-item").filter(
    has=page.locator(
      'a[href="/1234567890123/"]'
    )
  )
  
  produit.get_by_role("link", name="Voir les détails").click()

  expect(page).to_have_url("http://127.0.0.1:8000/1234567890123/")


  expect(page.locator("h1")).to_have_text("Coca-Cola")
  expect(page.locator(".code")).to_have_text("Article n° 1234567890123")

  nutriscore_info = page.locator(".info").filter(has_text="Nutriscore")
  expect(nutriscore_info).to_contain_text("Nutriscore :")
  expect(nutriscore_info).to_contain_text("E")

  categorie_info = page.locator(".info").filter(has_text="Catégorie(s)")
  expect(categorie_info).to_contain_text("Catégorie(s) :")
  expect(categorie_info).to_contain_text("Boissons")
    
  expect(page.locator(".ingredients")).to_have_text("Eau, sucre, colorant (caramel E150d), acidifiant (acide phosphorique), arômes naturels (dont caféine).")
