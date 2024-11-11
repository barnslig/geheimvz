import "./main.css";

const initPatternBg = () => {
  const pattern = document.getElementById(
    "bg-pattern"
  ) as HTMLTemplateElement | null;

  if (!pattern) {
    return;
  }

  const style = getComputedStyle(document.body);
  const tmpl = pattern.content.cloneNode(true) as Element;
  const svg = tmpl.querySelector("svg") as SVGElement;

  svg.style.fill = `rgb(${style.getPropertyValue("--colors-base-300")})`;

  const bg = btoa(svg.outerHTML);
  document.body.style.background = `rgb(var(--colors-base-200)) url(data:image/svg+xml;base64,${bg})`;
};

const initInsertText = () => {
  const btns = document.querySelectorAll<HTMLElement>(
    "[data-insert-text][data-insert-text-into]"
  );
  btns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const text = btn.dataset.insertText;
      const targetId = btn.dataset.insertTextInto;
      if (!text || !targetId) {
        return;
      }

      const target = document.getElementById(
        targetId
      ) as HTMLInputElement | null;
      if (!target) {
        return;
      }

      target.setRangeText(
        text,
        target.selectionStart || 0,
        target.selectionEnd || 0,
        "end"
      );
      target.focus();
    });
  });
};

const initCopyToClipboard = () => {
  const btns = document.querySelectorAll<HTMLElement>(
    "[data-copy-to-clipboard]"
  );
  btns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const text = btn.dataset.copyToClipboard;
      if (text) {
        navigator.clipboard.writeText(text);
      }
    });
  });
};

initPatternBg();
initInsertText();
initCopyToClipboard();
