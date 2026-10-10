(() => {
  const messagesEl = document.getElementById('messages');
  const form = document.getElementById('composer');
  const input = document.getElementById('prompt');
  const sendBtn = document.getElementById('send');
  const history = [];
  let busy = false;

  const scrollToEnd = () => { messagesEl.scrollTop = messagesEl.scrollHeight; };

  function resize() {
    input.style.height = 'auto';
    input.style.height = `${Math.min(input.scrollHeight, 128)}px`;
  }

  function addUser(text) {
    document.getElementById('empty-state')?.remove();
    const el = document.createElement('div');
    el.className = 'msg-user';
    el.textContent = text;
    messagesEl.append(el);
  }

  function addAssistant() {
    const wrap = document.createElement('div');
    wrap.className = 'msg-assistant';
    const label = document.createElement('span');
    label.className = 'msg-label';
    label.textContent = 'ZadAI';
    const body = document.createElement('div');
    body.className = 'msg-body';
    body.append(document.getElementById('thinking-tpl').content.cloneNode(true));
    wrap.append(label, body);
    messagesEl.append(wrap);
    return body;
  }

  async function send(text) {
    text = text.trim();
    if (busy || !text) return;
    busy = true;
    sendBtn.disabled = true;
    input.value = '';
    resize();

    history.push({ role: 'user', content: text });
    addUser(text);
    const body = addAssistant();
    scrollToEnd();

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: history.slice(-40) }),
      });
      if (res.status === 401) {
        window.location.href = '/login?next=/chat';
        return;
      }
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(typeof data.detail === 'string' ? data.detail : 'Erro ao falar com o ZadAI.');
      body.textContent = data.reply;
      history.push({ role: 'assistant', content: data.reply });
    } catch (err) {
      history.pop(); // a pergunta que falhou não entra no contexto
      body.textContent = err instanceof TypeError ? 'Sem conexão com o servidor. Tente de novo.' : err.message;
      body.classList.add('msg-error');
    } finally {
      busy = false;
      sendBtn.disabled = false;
      input.focus();
      scrollToEnd();
    }
  }

  form.addEventListener('submit', (e) => { e.preventDefault(); send(input.value); });
  input.addEventListener('input', resize);
  input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) {
      e.preventDefault();
      form.requestSubmit();
    }
  });
  document.querySelectorAll('[data-suggestion]').forEach((btn) => {
    btn.addEventListener('click', () => send(btn.dataset.suggestion));
  });
})();
