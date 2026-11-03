# Session 2026-11-03: opening a Myo and replacing its cells

**Type:** research and hands-on guidance, before the first cell swap.
**State at the end:** the right-hand wide pod is open, the old cell's wires are cut, and the new cell's black wire is soldered to the black stub (tug test not yet done). White → yellow and red → red remain; see § Where the swap stands.

## What was found

### The new cells
Cameron Sino CS-MYG100RC (Nextbatt packaging, EAN 4894128121602), 3.7 V, limited charge voltage 4.2 V. Each has **three bare tinned wires**, ends taped with kapton: red (+), black (−), white (most likely a temperature sensor). They are soldered in, not plugged.

### Where the cells are
In the **two pods directly either side of the logo pod**. Evidence, strongest first:
1. Thalmic's FCC filing 2ACKV-TL9B, internal photos dated 2014-07-08 (`fcc_2ACKV-TL9B_internal_photos_2014-07-08.pdf`, illustration 5): the main board with one cell on each side, each cell lying on a sensor board, joined to the main board by a short flex cable. The unit is a pre-production test sample (PCB rev D4, temporary antenna connector).
2. Thalmic's 2014 prototype history (BetaKit): "The larger pod in the middle contains the processing board, and the adjacent pods contained the batteries."
3. Size: a 17 mm wide cell fits only the wide pods; the band has three wide pods with the logo pod in the middle (Beebom review).

### How the original cells connect
FCC illustration 5 (zoomed): each original cell's three wires (black, yellow, red) are soldered to pads on the pod's sensor board. The new cell's white wire takes the yellow one's place. Adafruit's video narration (subtitles saved here) confirms "a three pin connector", which Lady Ada guesses is a temperature sensor or balancing line, and that the two 260 mAh cells are charged separately. The original cell label (Visconti et al. 2018, fig. 33A): "EVE 571830 144440100156 260mAh 3.7V".

### How the band is built
Thalmic's patent US 9,600,030 describes **two elastic bands** ("adaptive couplers") running along the pods, the elastomer overmoulded around a flexible printed circuit. OHM, the industrial designers: "an elastomeric band with an embedded flex circuit wraps around and holds the electronic outer plates." Adafruit's photos show one pleated band still carrying the pods and the orange flex, and a separate rubber band cut once and pulled off.

### How others opened the pods
**Nobody has described it.** Searched in English, Chinese and Japanese: forums, Reddit, Hackaday, Instructables, academic papers, YouTube. Only two sources show opened pods, and neither says how:
- Adafruit (2016): cut a band to lay the ring flat; pod shells prised apart; some shells show residue that looks like adhesive.
- The FCC lab (2014): the logo pod's outer plate off while the rubber around it stays whole.
Visconti et al. 2018 reuse Adafruit's photos. So opening the cell pods **probably needs no cut** (confirmed below); how the outer plate is held was unknown until then.

**How the outer plate is held: confirmed 2026-11-03 by opening one.** Fredrik opened the right-hand wide pod beside the logo pod (the guess about which pods hold cells was right). The plate has **two clip hooks at each short end** and a **bead of adhesive along both long edges**; its inside face is clean. The earlier reading of Adafruit's photo, glue across the whole face, was wrong: the grey piece in that photo is something else. What worked: slicing the adhesive along the long sides with a scalpel, the short ends left alone, then lifting. The cell sits in the pod with its wire end toward the flex cable.

**The original cell:** "EVE 571830 1430101511 260mAh 3.7V", not swollen. At its wire end sits the cell's own protection board under kapton (silkscreen C1, U1, U2, R1–R3, C2, "-B"); the three wires leave that board.

## The plan before opening (superseded: what worked is in § How the outer plate is held)
1. Battery pod = one of the two wide pods beside the logo pod.
2. The seam is very thin. Start it with a scalpel used only as a wedge, at most 1–2 mm deep, angled away from the cell underneath (a punctured LiPo cell can catch fire).
3. Do not lever with the blade (it snaps, and a snapped tip flies). Warm the plate until it is warm to the touch, then slice along the seam to cut the glue, and lever only with plastic. A suction cup on the smooth plate, and a drop of isopropyl alcohol in the seam to soften the adhesive, are the usual phone-repair aids.
4. If it will not give, it is glued: warm lightly with a hairdryer, no warmer than a cup of tea you can hold.
5. Photograph every step; this will be the first documented Myo cell replacement.
6. Close with a flexible glue (silicone-based or E6000-type), not superglue.

## Where the swap stands (2026-11-03, night)

- Done: pod opened; old wires cut near the old cell (black, yellow, red); black stub stripped about 2 mm and tinned; new black wire soldered to it, lying side by side with about 2 mm overlap.
- Left: give the black joint a light tug; white → yellow stub; red → red stub last (new red stays taped until then); insulate each joint with narrow kapton strips; test (USB charge, then unplugged the logo should pulse blue; the bridge's `bridge.log`); clip the lid back.
- What went wrong at the bench, worth knowing for the next person:
  - A solder blob melted onto a stub's insulation never wets the copper and drops off. Strip 1–2 mm first.
  - Solder cannot bridge a gap. Lay the wires side by side and tape the long new wire about 1 cm back so its tip presses on the stub; never try to move the short stub.
  - The kit iron (Luxorparts Lödkolvset 30 W, fixed temperature) with its lead-free solder oxidised its tip black after many attempts; then solder would not melt or stick. Each wipe on the wet sponge also cools a 30 W iron for 15–20 s.
- Morning start: with the iron cold, scrape or sand the point back to shiny metal; hold solder against the point and plug in, so it tins as it heats; keep a film of solder on the tip from then on. If it still will not tin, the tip is spent (Kjell spare tip 40068). Leaded solder (melts at about 183 °C against about 220 °C) would make the whole job easier.

## How the session went wrong, and the lesson

The cells were ordered on 2026-10-28 on Gemini's advice, before the 2026-11-02 research. That research did find that Adafruit cut the band open, but the report carried it as one clause in a paragraph, and the guide given on 2026-11-03 said "klipp i gummit" in passing. Fredrik's reaction when it landed:

> "men vafan detta kunde du ju gjort MYCKET tydligare innan jag ens beställde batterier arghhh"

The order itself predates the research, but the point stands: **a step that destroys or permanently changes the user's thing belongs at the top of the answer, stated as a cost, not inside a sentence about something else.** The research then also showed that the cut was probably not needed at all, which was found only because he pressed for more ("Research this extensively online. Ultrathink").

A second lesson, from the soldering: guidance given while his hands are busy names each part by what he can see, and says what the tape holds and where. After "tape the new wire to the pod's rim" he asked:

> "What do you mean, leave it alone? What do you mean by the pod? And how can I solder it if it's taped? And what is the pod's rim?"

"The pod" (the black plastic box the cell sat in) and "the rim" (its edge) had been used all session without ever being shown to him, and "tape it" did not say the tape goes 1 cm back from the joint. One step per message, in his words, worked; three numbered steps with an unglossed noun did not.

Two questions of his drove the useful finds:
- "Hur vet jag var jag ska klippa?!?!" (with Adafruit's photo) → reading the photo showed two separate rubber layers, and that the flex cable runs in the pleated band, not in the cut one.
- "Vilka segment sitter batterierna i?" → led to the FCC filing, the best evidence in the whole investigation.

## Cross-references
- `README.md` § Before opening a band (the resident summary of all of this).
- `reports/Myo wake and Bluetooth connection.md` and `research_notes/Myo wake and Bluetooth connection/revival_field_reports.md`: their "must cut" and "unknown whether soldered" lines are marked superseded and point here.
- Saved sources in this folder: the FCC internal photos and the Adafruit video subtitles. Visconti et al. 2018 is kept locally only (copyright): https://doi.org/10.21307/ijssis-2018-005
