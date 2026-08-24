from playwright.sync_api import Page, expect

BASE_URL = "http://127.0.0.1:8000"


def test_homepage(page: Page):
  page.goto(f"{BASE_URL}/")

  expect(page).to_have_title("Nutrifood")

def test_homepage_content(page: Page):
  page.goto(f"{BASE_URL}/")

  expect(page.locator("h1")).to_have_text("Bienvenue sur Nutrifood")
  expect(page.get_by_label("Nom du produit")).to_be_empty()
  expect(
    page.get_by_role(
      "link", name="Trouver une meilleure alternative"
    )
  ).to_have_attribute(
    "href", 
    "/alternative/"
  )

def test_rechercher_produit(page: Page):
  page.goto(f"{BASE_URL}/")

  page.get_by_label("Nom du produit").fill("Coca-Cola")
  page.get_by_role("button", name="Rechercher").click()

  expect(page).to_have_url(
    f"{BASE_URL}/recherche/?q=Coca-Cola"
  )

  expect(page.locator("h1")).to_have_text('Résultats de la recherche pour "Coca-Cola"')

  produits = page.locator(".produit-item")

  expect(produits).to_have_count(3)

  produit_test = page.locator(".produit-item").filter(
    has=page.locator('a[href="/1234567890123/"]')
  )

  expect(produit_test).to_contain_text("Coca-Cola")

  expect(produit_test).to_contain_text("Nutriscore: E")

  expect(produit_test).to_contain_text("Catégorie: Boissons")

  expect(
    produit_test.get_by_role(
      "link", 
      name="Voir les détails"
    )
  ).to_have_attribute(
    "href", "/1234567890123/"
  )

def test_detail_produit(page: Page):
  page.goto(f"{BASE_URL}/")

  page.get_by_label("Nom du produit").fill("Coca-Cola")
  page.get_by_role("button", name="Rechercher").click()

  produit = page.locator(".produit-item").filter(
    has=page.locator(
      'a[href="/1234567890123/"]'
    )
  )
  
  produit.get_by_role("link", name="Voir les détails").click()

  expect(page).to_have_url(
    f"{BASE_URL}/1234567890123/"
  )


  expect(page.locator("h1")).to_have_text("Coca-Cola")
  expect(page.locator(".code")).to_have_text("Article n° 1234567890123")

  nutriscore_info = page.locator(".info").filter(has_text="Nutriscore")
  expect(nutriscore_info).to_contain_text("Nutriscore :")
  expect(nutriscore_info).to_contain_text("E")

  categorie_info = page.locator(".info").filter(has_text="Catégorie(s)")
  expect(categorie_info).to_contain_text("Catégorie(s) :")
  expect(categorie_info).to_contain_text("Boissons")
    
  expect(page.locator(".ingredients")).to_have_text(
    "Eau, sucre, colorant (caramel E150d), acidifiant (acide phosphorique), arômes naturels (dont caféine)."
  )


def test_alternative(page: Page):
  page.goto(f"{BASE_URL}/")

  page.get_by_role("link", name="Trouver une meilleure alternative").click()

  expect(page).to_have_url(
    f"{BASE_URL}/alternative/"
  )

  expect(page.get_by_text("Produit à améliorer")).to_be_visible()

  expect(page.locator("h2").first).to_have_text("Produit recherché")
  expect(page.locator("h2").nth(1)).to_have_text("Meilleures alternatives")

  page.get_by_label("Produit à améliorer").fill("Coca")

  page.get_by_role("button", name="Trouver une meilleure alternative").click()

  expect(page).to_have_url(
    f"{BASE_URL}/alternative/?q=Coca"
  )

  expect(page.get_by_text("Coca-Cola - Nutriscore E")).to_be_visible()

  expect(page.locator("h2").nth(2)).to_have_text("Coca-Cola Zero")

  expect(page.get_by_text("Nutriscore: B")).to_be_visible()
  expect(page.get_by_text("Catégorie: Boissons")).to_be_visible()

  page.get_by_role("link", name="Retour à la recherche").click()

  expect(page).to_have_url(f"{BASE_URL}/")