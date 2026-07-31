// Episode 1: AI Agent — pptxgenjs deck builder
// Run: node build_deck.js
// Requires: pptxgenjs, react, react-dom, react-icons, sharp
// Output: AI_Agent_Lesson.pptx

const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const {
  FaRobot, FaFileExcel, FaFileWord, FaBolt, FaClipboardList,
  FaUserCheck, FaCogs, FaCheckCircle, FaDatabase,
  FaArrowRight, FaLightbulb, FaGraduationCap,
} = require("react-icons/fa");

// Ocean Gradient palette (consistent across series)
const NAVY = "21295C";
const DEEP_BLUE = "065A82";
const TEAL = "1C7293";
const ICE = "EAF2F5";
const WHITE = "FFFFFF";
const INK = "16202A";
const MUTED = "5B6B76";

async function iconPng(IconComp, color, sizePx = 256) {
  const svg = ReactDOMServer.renderToStaticMarkup(
    React.createElement(IconComp, { color: `#${color}`, size: sizePx })
  );
  const buf = await sharp(Buffer.from(svg)).resize(sizePx, sizePx).png().toBuffer();
  return "image/png;base64," + buf.toString("base64");
}

function iconCircle(slide, png, x, y, d, circleColor) {
  slide.addShape("ellipse", { x, y, w: d, h: d, fill: { color: circleColor }, line: { type: "none" } });
  const pad = d * 0.26;
  slide.addImage({ data: png, x: x + pad, y: y + pad, w: d - pad * 2, h: d - pad * 2 });
}

async function main() {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE";
  const W = 13.33;
  const FONT_HEAD = "Cambria";
  const FONT_BODY = "Calibri";

  const icons = {
    robot: await iconPng(FaRobot, WHITE),
    cogs: await iconPng(FaCogs, WHITE),
    check: await iconPng(FaCheckCircle, WHITE),
    database: await iconPng(FaDatabase, WHITE),
    arrow: await iconPng(FaArrowRight, DEEP_BLUE),
    bulb: await iconPng(FaLightbulb, WHITE),
    cap: await iconPng(FaGraduationCap, WHITE),
    clipboard: await iconPng(FaClipboardList, WHITE),
  };

  // Slide 1: Title
  {
    const s = pres.addSlide();
    s.background = { color: NAVY };
    iconCircle(s, icons.robot, W / 2 - 0.8, 0.65, 1.6, DEEP_BLUE);
    s.addText("What’s an AI Agent?", {
      x: 0.5, y: 3.1, w: W - 1, h: 1.3, align: "center",
      fontFace: FONT_HEAD, fontSize: 44, color: WHITE, bold: true,
    });
    s.addText("Episode 1 · featuring Mistral Studio", {
      x: 0.5, y: 4.5, w: W - 1, h: 0.5, align: "center",
      fontFace: FONT_BODY, fontSize: 16, color: ICE, italic: true,
    });
  }

  // Slide 2: Definition
  {
    const s = pres.addSlide();
    s.background = { color: NAVY };
    iconCircle(s, icons.bulb, 0.9, 2.55, 1.5, DEEP_BLUE);
    s.addText(
      "An AI agent is software that looks at a goal, figures out the steps to reach it, uses tools along the way, and checks its own results — without you spelling out every step.",
      { x: 2.8, y: 1.3, w: W - 3.5, h: 3.2, fontFace: FONT_HEAD, fontSize: 27, color: WHITE, lineSpacingMultiple: 1.25 }
    );
  }

  // Slide 3: Macro vs Agent
  {
    const s = pres.addSlide();
    s.background = { color: WHITE };
    s.addText("A macro vs. an agent", { x: 0.6, y: 0.5, w: W - 1.2, h: 0.7, fontFace: FONT_HEAD, fontSize: 32, color: NAVY, bold: true });
    const cols = [
      { title: "A Macro", rows: ["Follows exact pre-written steps", "Like a recipe card", "Breaks if anything is different"] },
      { title: "An AI Agent", rows: ["Decides its own steps toward a goal", "Like an assistant you hand a task to", "Adjusts the plan if something doesn't work"] },
    ];
    const colW = 5.4, gap = 0.6, startX = (W - (colW * 2 + gap)) / 2, colY = 1.6;
    cols.forEach((c, i) => {
      const x = startX + i * (colW + gap);
      s.addShape("roundRect", { x, y: colY, w: colW, h: 5.0, rectRadius: 0.12, fill: { color: i === 1 ? ICE : "F4F6F7" }, line: { type: "none" } });
      s.addText(c.title, { x: x + 0.4, y: colY + 0.35, w: colW - 0.8, h: 0.6, fontFace: FONT_HEAD, fontSize: 20, color: DEEP_BLUE, bold: true });
      c.rows.forEach((r, j) => {
        s.addText(r, { x: x + 0.5, y: colY + 1.15 + j * 1.15, w: colW - 1.0, h: 1.0, fontFace: FONT_BODY, fontSize: 15, color: INK, bullet: { code: "2022" }, valign: "top" });
      });
    });
  }

  // Slide 4: Mistral Studio
  {
    const s = pres.addSlide();
    s.background = { color: ICE };
    s.addText("Seen in a real product: Mistral Studio", { x: 0.6, y: 0.5, w: W - 1.2, h: 0.7, fontFace: FONT_HEAD, fontSize: 30, color: NAVY, bold: true });
    const rows = [
      { icon: icons.cogs, title: "Agent Runtime", body: "The engine that runs an agent's steps — the motor under the hood." },
      { icon: icons.check, title: "Judges", body: "Checks the agent's work and scores it — like spell-check, but for reasoning." },
      { icon: icons.database, title: "AI Registry", body: "A filing cabinet tracking every agent, model, and dataset a team has built." },
    ];
    rows.forEach((r, i) => {
      const y = 2.0 + i * 1.55;
      iconCircle(s, r.icon, 0.7, y, 1.05, DEEP_BLUE);
      s.addText(r.title, { x: 2.0, y: y - 0.05, w: 3.0, h: 1.05, valign: "middle", fontFace: FONT_HEAD, fontSize: 19, color: NAVY, bold: true });
      s.addText(r.body, { x: 5.1, y: y - 0.05, w: W - 5.7, h: 1.05, valign: "middle", fontFace: FONT_BODY, fontSize: 15, color: INK });
    });
  }

  // Slide 5: Recap
  {
    const s = pres.addSlide();
    s.background = { color: NAVY };
    iconCircle(s, icons.clipboard, W / 2 - 0.75, 1.5, 1.5, DEEP_BLUE);
    s.addText("Model talks. Agent walks — and writes down where it went.", {
      x: 0.5, y: 3.5, w: W - 1, h: 1.0, align: "center",
      fontFace: FONT_HEAD, fontSize: 28, color: WHITE, bold: true,
    });
    s.addText("Next: What's a “Model”? — the brain the agent uses to think.", {
      x: 0.5, y: 5.0, w: W - 1, h: 0.6, align: "center",
      fontFace: FONT_BODY, fontSize: 18, color: TEAL, italic: true,
    });
  }

  await pres.writeFile({ fileName: "AI_Agent_Lesson.pptx" });
  console.log("done — AI_Agent_Lesson.pptx");
}

main().catch(e => { console.error(e); process.exit(1); });
