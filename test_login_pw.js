const { chromium } = require('playwright');
const os = require('node:os');
const path = require('node:path');

(async () => {
  const browser = await chromium.launch({ headless: false });
  const context = await browser.newContext();
  const page = await context.newPage();

  try {
    console.log('1. Acessando a página de login...');
    await page.goto('http://localhost:3001/login');
    await page.waitForLoadState('networkidle');

    console.log('2. Preenchendo credenciais...');
    await page.getByLabel('E-mail').fill('diego@exemplo.com');
    await page.getByLabel('Senha').fill('senha123');

    console.log('3. Clicando em Entrar...');
    await page.getByRole('button', { name: 'Entrar' }).click();

    console.log('4. Aguardando redirecionamento para a home...');
    await page.waitForURL('http://localhost:3001/', { timeout: 10000 });

    console.log('5. Verificando se o nome do usuário aparece no topo...');
    const userNameElement = await page.locator('text=Diego');
    await userNameElement.waitFor({ state: 'visible', timeout: 5000 });
    console.log('SUCESSO: Redirecionado para a home e nome do usuário visível!');

    await page.screenshot({ path: path.join(os.tmpdir(), 'login-success.png'), fullPage: true });
  } catch (err) {
    console.error('FALHA NO TESTE:', err);
    await page.screenshot({ path: path.join(os.tmpdir(), 'login-failure.png'), fullPage: true });
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
