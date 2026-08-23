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

