# Session 2026-11-03: opening a Myo and replacing its cells

**Type:** research and hands-on guidance, before the first cell swap.
**State at the end:** the replacement cells are unpacked; Fredrik has found the seams of a battery pod's outer plate but has not opened it. His old phone-repair plastic opener is too thick for the seam.

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
Visconti et al. 2018 reuse Adafruit's photos. So opening the cell pods **probably needs no cut**; how the outer plate is held (clips, adhesive or both) is unknown.

## The working plan (untested)
1. Battery pod = one of the two wide pods beside the logo pod.
2. The seam is very thin. Start it with a scalpel used only as a wedge, at most 1–2 mm deep, angled away from the cell underneath (a punctured LiPo cell can catch fire).
3. Once a gap opens, work round the edge with thin plastic (a guitar pick, an old plastic card), never with the blade.
4. If it will not give, it is glued: warm lightly with a hairdryer, no warmer than a cup of tea you can hold.
5. Photograph every step; this will be the first documented Myo cell replacement.
6. Close with a flexible glue (silicone-based or E6000-type), not superglue.

## How the session went wrong, and the lesson

The cells were ordered on 2026-10-28 on Gemini's advice, before the 2026-11-02 research. That research did find that Adafruit cut the band open, but the report carried it as one clause in a paragraph, and the guide given on 2026-11-03 said "klipp i gummit" in passing. Fredrik's reaction when it landed:

> "men vafan detta kunde du ju gjort MYCKET tydligare innan jag ens beställde batterier arghhh"

The order itself predates the research, but the point stands: **a step that destroys or permanently changes the user's thing belongs at the top of the answer, stated as a cost, not inside a sentence about something else.** The research then also showed that the cut was probably not needed at all, which was found only because he pressed for more ("Research this extensively online. Ultrathink").

Two questions of his drove the useful finds:
- "Hur vet jag var jag ska klippa?!?!" (with Adafruit's photo) → reading the photo showed two separate rubber layers, and that the flex cable runs in the pleated band, not in the cut one.
- "Vilka segment sitter batterierna i?" → led to the FCC filing, the best evidence in the whole investigation.

## Cross-references
- `README.md` § Before opening a band (the resident summary of all of this).
- `reports/Myo wake and Bluetooth connection.md` and `research_notes/Myo wake and Bluetooth connection/revival_field_reports.md`: their "must cut" and "unknown whether soldered" lines are marked superseded and point here.
- Saved sources in this folder: the FCC internal photos and the Adafruit video subtitles. Visconti et al. 2018 is kept locally only (copyright): https://doi.org/10.21307/ijssis-2018-005
