# GDADA game-design anchor graph

Solid arrows ground or extend; dotted arrows are counterpoints. Copy labels exactly. Status classes for a live graph:
`visited`, `kept`, `adapted`, `scrapped`.

```mermaid
flowchart TB
  subgraph EXPERIENCE["PLAYER EXPERIENCE"]
    flow["Flow: challenge matched to skill, clear goals, instant feedback (Csikszentmihalyi, Flow)"]
    fun["Fun as learning patterns; boredom when mastered (Koster, A Theory of Fun for Game Design)"]
    ssd["Self-determination: autonomy, competence, relatedness (Ryan and Deci)"]
    lenses["The Lenses: surprise, curiosity, endogenous value, problem statement (Schell, The Art of Game Design)"]
    cozy["Cozy play: comfort, mastery without threat, a place to return to (Animal Crossing, Stardew Valley, Unpacking)"]
  end
  subgraph MECH["MECHANICS"]
    mda["MDA: mechanics, dynamics, aesthetics (Hunicke, LeBlanc, Zubek)"]
    rules["Rules, play and culture; meaningful play (Salen and Zimmerman, Rules of Play)"]
    decisions["Interesting decisions (Sid Meier)"]
    machinations["Feedback loops and economies (Adams and Dormans, Game Mechanic Design and Level Design)"]
    verbs["Verbs first: the core verb must be pleasant alone (Fullerton, Game Design Workshop)"]
    halfreal["Half-Real: real rules, fictional world (Juul)"]
  end
  subgraph FEEL["FEEL"]
    gamefeel["Game Feel: input, response, context, polish (Swink)"]
    juice["Juice it or lose it: feedback in layers (Jonasson and Purho)"]
    anim["Twelve principles: anticipation, squash, follow-through (Thomas and Johnston, The Illusion of Life)"]
    sound["Sound as feedback and mood (Collins, Game Sound)"]
  end
  subgraph WORLD["WORLD AND AGENTS"]
    envstory["Environmental storytelling (Jenkins, Game Design as Narrative Architecture)"]
    agents["Believable agents: readable intent, personality in movement (Mateas and Stern, Facade; Millington, AI for Games)"]
    steering["Steering behaviours: seek, arrive, avoid (Reynolds)"]
    persuasive["Procedural rhetoric: rules that argue (Bogost, Persuasive Games)"]
    readable["Readability: silhouette, contrast, one focal point (Solarski, Drawing Basics and Video Game Art)"]
  end
  subgraph LEVEL["LEVEL AND TEACHING"]
    mario["Teach by play: introduce, develop, twist, conclude (Nintendo level design; Kishotenketsu)"]
    ramp["Difficulty curve and pacing (Schell; Swink)"]
    onboarding["No tutorial text: the first minute teaches by doing (Valve, Portal level design)"]
    proc["Procedural generation with a solver behind it (Shaker, Togelius and Nelson, Procedural Content Generation in Games)"]
  end
  subgraph ACCESS["ACCESS"]
    gag["Game Accessibility Guidelines: basic, intermediate, advanced"]
    affordance["Affordances, signifiers, feedback (Norman, The Design of Everyday Things)"]
    krug["Don't make me think (Krug)"]
  end
  subgraph ENG["ENGINEERING"]
    loop["The game loop and update method (Nystrom, Game Programming Patterns)"]
    timestep["Fix your timestep (Fiedler)"]
    determinism["Deterministic simulation: same seed, same result"]
    perf["Frame budget: 16.7 ms and no hitch in the worst scene"]
  end
  subgraph TEST["PLAYTEST AND RISK"]
    playtest["Playtesting: watch, do not explain (Fullerton; Schell)"]
    bots["Bot playtesting: perfect bot proves solvable, noisy bot shows the curve"]
    premortem["Premortem (Gary Klein, Performing a Project Premortem)"]
    scope["Scope: cut to the loop, then the juice (Brooks, The Mythical Man-Month; Shape Up)"]
  end

  flow --> ramp
  fun --> verbs
  ssd --> decisions
  lenses --> mda
  cozy --> decisions
  mda --> rules
  rules --> machinations
  verbs --> gamefeel
  gamefeel --> juice
  juice --> anim
  anim --> sound
  agents --> steering
  agents --> anim
  envstory --> readable
  mario --> onboarding
  onboarding --> ramp
  proc --> bots
  bots --> determinism
  determinism --> loop
  loop --> timestep
  timestep --> perf
  affordance --> krug
  gag --> affordance
  playtest --> bots
  premortem --> scope
  halfreal --> envstory
  persuasive --> rules
  readable --> affordance

  fun -.-> persuasive
  gamefeel -.-> rules
  cozy -.-> decisions
  flow -.-> fun
  juice -.-> scope
  proc -.-> envstory
  ramp -.-> cozy
```

## Panel seats (one authority per seat)

| Seat | Work | What it argues from |
|---|---|---|
| Flow | Csikszentmihalyi, *Flow* | Is challenge matched to skill, are goals clear, is feedback instant? |
| Learner | Koster, *A Theory of Fun* | What pattern is the player learning, and when is it mastered? |
| Lenses | Schell, *The Art of Game Design* | Surprise, curiosity, endogenous value; the problem statement |
| Rules | Salen and Zimmerman, *Rules of Play* | Does each rule earn its place; is the play meaningful? |
| Feel | Swink, *Game Feel* | Input, response and polish; what does the verb feel like alone? |
| Decisions | Meier, interesting decisions | What is the player choosing, and does it cost something? |
| Rhetoric | Bogost, *Persuasive Games* | What do the rules say, and does the theme agree? |
| Affordance | Norman, *The Design of Everyday Things* | Can a stranger tell what is clickable and what happened? |
| Access | Game Accessibility Guidelines | Who cannot play this, and what is the cheapest fix? |
| Agents | Reynolds and Mateas, believable agents | Do the characters read as alive: intent, personality, no jitter? |
| Engineer | Nystrom and Fiedler | Is the loop stable, deterministic and inside the frame budget? |
| Cut | Brooks, scope | What can go and leave the loop standing? |
| Premortem | Klein | How does this fail with a real player? |

Dotted pairs usable for the mode rule: Feel and Rules, Learner and Rhetoric, Flow and Learner, Decisions and Cozy.
