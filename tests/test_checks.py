from urlrisk.scorer import score_url


def reasons(url):
    return [f.check for f in score_url(url).findings]


def test_legit_site_is_low():
    assert score_url("https://www.google.com/search?q=cats").level == "LOW"


def test_ip_host():
    assert "ip_host" in reasons("http://192.168.1.1/login")


def test_at_symbol():
    assert "userinfo" in reasons("http://paypal.com@evil.ru/")


def test_brand_in_subdomain():
    assert "brand_misuse" in reasons("https://paypal.com.evil.ru/signin")


def test_lookalike_digit():
    assert "typosquat" in reasons("https://paypa1.com")


def test_exact_match_not_flagged():
    assert "typosquat" not in reasons("https://paypal.com")


def test_phishy_url_is_high():
    r = score_url("http://paypa1-secure.login-verify.xyz/update")
    assert r.level == "HIGH"
    