# Nano Banana Pro MCP -- Complete Guide

> **Nano Banana** is Google's codename for Gemini's native image generation capabilities.
> The **nano-banana-pro-mcp** server exposes these capabilities as tools inside Claude Code, Cursor, or any MCP-compatible client.

---

## Table of Contents

1. [What Is It](#what-is-it)
2. [Models & Pricing](#models--pricing)
3. [Setup](#setup)
4. [Available Tools](#available-tools)
5. [Prompting Fundamentals](#prompting-fundamentals)
6. [Making Images Look Hyper-Realistic (Not AI)](#making-images-look-hyper-realistic-not-ai)
7. [Using Reference Images](#using-reference-images)
8. [Multi-Image Composition](#multi-image-composition)
9. [Image Editing](#image-editing)
10. [Prompt Templates by Use Case](#prompt-templates-by-use-case)
11. [Configuration Options](#configuration-options)
12. [Batch Generation Workflow](#batch-generation-workflow)
13. [Background Removal with rembg](#background-removal-with-rembg)
14. [Limitations & Best Practices](#limitations--best-practices)

---

## What Is It

The `nano-banana-pro-mcp` is an MCP server that connects Google Gemini's image generation models to your AI coding assistant. It provides three tools:

- **`generate_image`** -- Create images from text prompts (optionally guided by reference images)
- **`edit_image`** -- Modify existing images based on text instructions
- **`describe_image`** -- Analyze images and return text descriptions

The server handles all the Gemini API communication, base64 encoding/decoding, and file I/O so you can just describe what you want in natural language.

---

## Models & Pricing

| Model | ID | Speed | Max Resolution | Max Reference Images | Cost | Best For |
|---|---|---|---|---|---|---|
| **Nano Banana Pro** | `gemini-3-pro-image-preview` | 10-30+ sec | 4K (4096x4096) | 14 | ~$0.05-$0.24/image | Photorealism, complex scenes, text rendering, precision work |
| **Nano Banana** | `gemini-2.5-flash-preview-05-20` | Sub-second to 3 sec | 1024x1024 | 3 | ~$0.03-$0.04/image | Speed, iteration, drafts, high-volume |
| **Fallback** | `gemini-2.0-flash-exp` | Variable | 1024x1024 | Limited | Free tier available | Testing, basic generation |

**Nano Banana Pro** is the default and recommended model. It uses a "Thinking" reasoning layer before generating, which means it follows complex instructions more accurately and produces higher-fidelity output.

All models include invisible **SynthID watermarks** on generated images.

---

## Setup

### Prerequisites

- Node.js 18+
- Google Gemini API key (free from https://aistudio.google.com/apikey)

### Claude Code CLI (one-liner)

```bash
claude mcp add nano-banana-pro --env GEMINI_API_KEY=your_api_key_here -- npx @rafarafarafa/nano-banana-pro-mcp
```

### Claude Desktop

Add to your config file:
- **macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "nano-banana-pro": {
      "command": "npx",
      "args": ["-y", "@rafarafarafa/nano-banana-pro-mcp"],
      "env": {
        "GEMINI_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

### Cursor IDE

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "nano-banana-pro": {
      "command": "npx",
      "args": ["-y", "@rafarafarafa/nano-banana-pro-mcp"],
      "env": {
        "GEMINI_API_KEY": "your_api_key_here"
      }
    }
  }
}
```

After adding, restart your client or reload MCP servers.

---

## Available Tools

### 1. `generate_image` -- Text-to-Image

Generate an image from a text prompt. Optionally provide reference images to guide the output.

| Parameter | Required | Description |
|---|---|---|
| `prompt` | Yes | Description of the image to generate |
| `model` | No | Model ID (default: `gemini-3-pro-image-preview`) |
| `aspectRatio` | No | `"1:1"`, `"3:4"`, `"4:3"`, `"9:16"`, `"16:9"` |
| `imageSize` | No | `"1K"`, `"2K"`, `"4K"` (must be uppercase K) |
| `images` | No | Array of reference images `[{ data: "base64...", mimeType: "image/png" }]` |
| `outputPath` | No | File path to save the image (e.g., `./output/hero.png`) |

### 2. `edit_image` -- Edit Existing Images

Edit one or more images based on text instructions.

| Parameter | Required | Description |
|---|---|---|
| `prompt` | Yes | Instructions for how to edit the image(s) |
| `images` | Yes | Array of images to edit `[{ data: "base64...", mimeType: "image/png" }]` |
| `model` | No | Model ID (default: `gemini-3-pro-image-preview`) |
| `outputPath` | No | File path to save the edited image |

### 3. `describe_image` -- Analyze Images

Analyze and describe one or more images. Returns text only (no image output).

| Parameter | Required | Description |
|---|---|---|
| `images` | Yes | Array of images to analyze |
| `prompt` | No | Custom analysis prompt (default: general description) |
| `model` | No | Model ID |

---

## Prompting Fundamentals

### The Golden Rule

> **Describe the scene as a narrative paragraph, not a keyword list.**
> Gemini's strength is deep language understanding. A flowing description produces more coherent images than disconnected keywords.

### The 7 Core Elements

Every strong prompt should address as many of these as relevant:

1. **Subject** -- Who or what is the focus. Be specific.
   - Weak: "a person"
   - Strong: "a woman in her 30s with freckles and auburn hair"

2. **Composition** -- How the shot is framed.
   - Examples: extreme close-up, wide shot, low angle, bird's eye view, portrait, 3/4 view

3. **Action** -- What is happening in the scene.
   - Examples: mid-laugh reaching for a coffee cup, running through rain

4. **Location** -- Where the scene takes place with specific environmental details.
   - Examples: a sun-drenched Parisian sidewalk cafe, a misty Pacific Northwest forest trail

5. **Style** -- The overall aesthetic.
   - Examples: photorealistic, 3D animation, film noir, watercolor, 1990s product photography

6. **Technical/Refinements** -- Camera settings, lighting, constraints.
   - Examples: "85mm f/1.8 lens, shallow depth of field", "golden hour backlighting", "Kodak Portra 400 color grading"

7. **Photographer Perspective** -- Who is taking the photo and why. This grounds the composition in a believable point of view.
   - Examples: "snapped by a friend standing nearby", "taken from the garage looking out", "captured on a phone by a passerby"

### Constraints & Exclusions

Use **natural language** to state what you don't want. Don't use negative prompt syntax -- just describe it clearly:

- "Do not include any text or watermarks"
- "The background must be plain white with no distractions"
- "Keep the original lighting unchanged"
- "No other people in the frame"

---

## Making Images Look Hyper-Realistic (Not AI)

This is the most important section if you want images that pass as real photographs. AI-generated images have telltale signs: over-smoothed skin, perfect symmetry, unnatural lighting, sterile backgrounds, and overly saturated colors. Here's how to counteract every one of them.

### 1. Specify Camera Equipment

Reference specific cameras, lenses, and aperture settings. This forces the model to replicate the optical characteristics and color science of real photographic equipment rather than producing generic "digital art."

```
Shot on a Canon EOS R5, 85mm f/1.8 lens, natural lighting
```

**Camera/lens combos by purpose:**

| Purpose | Prompt Language |
|---|---|
| Portrait with blurred background | "85mm lens, f/1.4 aperture, shallow depth of field, creamy bokeh" |
| Wide environmental shot | "24mm wide-angle lens, deep depth of field, f/8" |
| Dramatic close-up | "macro lens, extreme close-up, razor-thin DOF" |
| Cinematic feel | "anamorphic lens, 2.39:1 aspect ratio, cinematic color grading" |
| Documentary style | "35mm lens, natural lighting, slight handheld motion" |
| Product photography | "100mm macro lens, f/11, focus-stacked, studio strobe lighting" |

### 2. Request Natural Imperfections

AI defaults to sterile perfection. Counter this by explicitly requesting subtle human flaws:

- "Natural skin texture with visible pores, fine wrinkles, and slight blemishes"
- "Slight asymmetry in facial features"
- "Visible freckles and sun spots"
- "Flyaway hairs catching the light"
- "Fabric with natural creases and folds"
- "Slightly chipped paint on the door frame"

### 3. Reference Film Stocks and Analog Photography

Film stock references introduce organic grain, warmth, and color characteristics that feel authentically handcrafted:

- **Kodak Portra 400** -- warm skin tones, soft pastels, classic portrait film
- **Fuji Pro 400H** -- cooler tones, slightly desaturated, editorial feel
- **Kodak Ektar 100** -- vivid colors, fine grain, landscape photography
- **Ilford HP5** -- classic black and white, visible grain, high contrast
- **Leica M6 / Contax T2** -- referencing specific cameras adds character

```
Color grading reminiscent of Kodak Portra 400. Slight film grain visible.
Shot on a Leica M6 with natural window light.
```

### 4. Use Rich Environmental Details

Embed subjects in richly described, imperfect settings. Specific tactile details create believable, lived-in scenes:

- "Dusty windows with fingerprints catching afternoon light"
- "Weathered wooden table with coffee ring stains"
- "Steam rising from a chipped ceramic mug"
- "Mismatched crockery on a cluttered kitchen counter"
- "Peeling wallpaper in a warm-toned vintage apartment"

### 5. Describe Materials with Specificity

Don't just say "leather jacket" -- describe the material's condition and texture:

- "Full-grain brown leather with visible grain texture, worn elbows, slightly faded"
- "Chunky cable-knit wool sweater with a small unraveled thread at the hem"
- "Matte brushed aluminum with micro-scratches from daily use"

### 6. Use Candid, Action-Oriented Language

Override AI's tendency toward stiff, posed compositions:

- "Caught mid-stride walking through a crosswalk"
- "Genuine laughter, eyes crinkled, looking slightly away from camera"
- "Leaning against a wall, scrolling their phone, not aware of the camera"
- "Mid-conversation, gesturing with one hand"

### 7. Use Specific Lighting Terminology

Lighting is the single biggest factor in photorealism. Be precise:

- "Golden hour backlighting creating long shadows and lens flare"
- "Soft diffused overcast natural light, no harsh shadows"
- "Dramatic side lighting from a single window, deep shadows on one side"
- "Practical lighting from a desk lamp casting warm pools of light"
- "Volumetric light rays filtering through dust particles in a barn"
- "Rim lighting outlining the subject's hair and shoulders"
- "Dappled sunlight through tree canopy creating irregular shadow patterns"

### 8. Avoid These AI Giveaway Terms

Paradoxically, these common AI prompt terms push output TOWARD a synthetic look:

| Avoid | Use Instead |
|---|---|
| "8K ultra-HD" | "sharp focus, natural resolution" |
| "hyper-detailed" | Describe specific details you want |
| "masterpiece" | Describe the specific quality characteristics |
| "best quality" | Reference a specific camera/film stock |
| "ultra-realistic" | "photorealistic, shot on [camera model]" |
| "perfect lighting" | Describe the specific lighting setup |
| "flawless skin" | "natural skin texture with visible pores" |

### 9. The UGC / Customer Photo Shortcut

For authentic, user-generated-content style photos (reviews, testimonials, social proof), these phrases work remarkably well:

- **"Realistic, taken with an iPhone"** -- the single most effective phrase for shifting output from polished stock to authentic UGC
- **"Candid customer photo feel"** -- reinforces casual, unposed aesthetic
- **"Slightly imperfect framing"** -- prevents overly perfect compositions
- **"Natural and authentic"** -- general authenticity signal
- **"Snapped by a friend standing nearby"** -- grounds the photographer's POV

### Complete Hyper-Realistic Prompt Example

Weak prompt:
```
realistic photo of a woman in a cafe
```

Strong prompt:
```
A photorealistic candid portrait of a woman in her early 30s sitting
at a weathered wooden table in a Parisian sidewalk cafe, caught
mid-laugh while reaching for her espresso cup. Morning golden hour
sunlight filtering through the striped awning creates warm dappled
shadows across her face. Natural skin texture with slight freckles
across her nose, visible pores, fine smile lines around her eyes.
She's wearing a cream linen blouse with a natural wrinkle at the
elbow and a thin gold necklace. A half-eaten croissant and a folded
newspaper sit on the table beside a small ceramic vase with a wilting
daisy. Shot on a Canon EOS R5 with an 85mm f/1.8 lens creating soft
creamy bokeh in the background where other patrons and potted plants
are gently blurred. Natural color grading reminiscent of Kodak Portra
400 film stock with subtle warm tones and gentle grain. The photo
looks like it was taken by a friend sitting across the table.
```

---

## Using Reference Images

Reference images are the key to generating **consistent, accurate** depictions of specific items, people, or scenes. Without a reference, the model will hallucinate details -- wrong shape, wrong color, wrong proportions.

### Reference Image Capacity by Model

| Model | Max References | Fidelity |
|---|---|---|
| Nano Banana Pro (`gemini-3-pro-image-preview`) | Up to 14 total (6 objects + 5 humans) | High -- preserves fine details |
| Nano Banana (`gemini-2.5-flash-preview-05-20`) | Up to 3 | Moderate -- captures general appearance |
| Fallback (`gemini-2.0-flash-exp`) | Limited | Basic |

### How Reference Images Work

When you provide reference images, the AI assistant (Claude, Cursor, etc.) will:

1. Read the image file(s) from disk
2. Convert them to base64 internally
3. Pass them to the tool's `images` parameter
4. Save the output to the specified `outputPath`

You just need to tell the assistant which files to use. Example conversation:

```
You: Read the product photo at ./images/product.png and generate a
lifestyle shot of someone using it outdoors at sunset. Save to
./output/lifestyle-shot.png
```

### Single Reference Image (Exact Item Recreation)

Use one reference image when you want the exact item placed in a new context:

```
A professional product photograph of the item shown in the reference
image, placed on a clean white marble countertop. Soft studio lighting
from the upper left, slight shadow underneath. The item should match
the reference exactly in shape, color, and proportions. Shot with a
100mm macro lens at f/8. Save to ./output/product-marble.png
```

### Two Reference Images (Item + Context or Item + Style)

Use two references to combine elements:

**Item + Scene:**
```
Take the product from the first image and place it in the outdoor
scene from the second image. The product should be held in someone's
hand, naturally integrated into the environment. Match the lighting
and color temperature of the outdoor scene.
```

**Item + Style:**
```
Create an image of the product from the first image in the artistic
style shown in the second image. Preserve the product's exact design,
colors, and proportions while applying the stylistic treatment.
```

**Person + New Environment:**
```
Generate a professional headshot of the person from the first image
in the office setting shown in the second image. Warm natural lighting,
Canon EOS R5, 85mm lens, f/2.0. Preserve the person's exact facial
features, hair, and skin tone.
```

### Three Reference Images (Multi-Angle or Multi-Element)

Use three references for maximum consistency:

**Multi-Angle Product Recreation:**
```
Generate a new 45-degree angle view of the product shown in the three
reference photos (front view, side view, detail view). Maintain exact
design details, colors, branding, and proportions. Studio lighting,
white background. Save to ./output/product-angle.png
```

**Person + Item + Scene:**
```
Place the person from the first image holding the product from the
second image in the environment shown in the third image. Natural
pose, candid feel, golden hour lighting. The person's features and
the product's design should match the references exactly.
```

### Best Practices for Reference Images

1. **Use clear, well-lit reference photos** -- avoid heavy shadows, obstructions, or motion blur
2. **Front-facing photos deliver the best fidelity** for both people and products
3. **Multiple angles improve accuracy** -- if you have front + side + detail shots, use all of them
4. **Be explicit about what to preserve** -- "maintain the exact facial features", "keep the same clothing", "preserve the product design exactly as shown"
5. **Reference images by ordinal position** -- "the first image", "the second image", not "image 1" or "image A"
6. **Always pass product references for lifestyle shots** -- without a reference, generating 7 product-in-use photos produces 7 different-looking products
7. **For people: avoid sunglasses and heavy shadows** in reference photos for cleanest face reproduction

### Reference Image Quality Checklist

- [ ] High resolution (at least 512x512, ideally higher)
- [ ] Good, even lighting
- [ ] Clear/sharp (no motion blur)
- [ ] Subject fills a good portion of the frame
- [ ] No heavy obstructions (sunglasses, hats covering face, etc.)
- [ ] Consistent quality across multiple references

---

## Multi-Image Composition

Nano Banana Pro supports up to **14 reference images** in a single generation:
- Up to **6 images of objects** with high-fidelity inclusion
- Up to **5 images of humans** for character consistency

### How to Reference Images in Prompts

Images are numbered by the order they appear in the `images` array, starting with "the first image", "the second image", etc.

**Key pattern:**
```
Take the [element] from the first image and place it
[in/on/with] the [element] from the second image.
The final image should be [description].
```

### Composition Examples

**Combine product + scene:**
```
Take the fire tool from the first image and place it in the outdoor
scene from the second image. Make it look like the tool is being used
in a controlled burn. Match the lighting of the outdoor scene.
```

**Swap elements between images:**
```
Take the dress from the first image and put it on the person in the
second image. Generate a realistic full-body e-commerce shot with
studio lighting.
```

**Style transfer from one image to another:**
```
Use the art style and color palette from the first image. Apply that
style to recreate the scene in the second image.
```

**Product lineup from multiple images:**
```
Create a product lineup photograph combining the items from all
provided images. Arrange them left to right on a clean white surface
with consistent studio lighting. The first image's item should be
in the center and largest.
```

**Character consistency across scenes:**
```
An office group photo of the people from the provided images. They
are standing together in front of a modern office building, smiling
naturally. Preserve each person's exact features.
```

### Image Reference Cheat Sheet

| What You Want | How to Prompt |
|---|---|
| Use object from image 1 | "Take the [object] from the first image..." |
| Use person from image 2 | "...and place the person from the second image..." |
| Match style of image 3 | "Apply the art style from the third image..." |
| Match lighting of image 1 | "Match the lighting and shadows from the first image..." |
| Keep pose from image 2 | "Keep the pose from the second image..." |
| Combine all images | "Combine all provided images into one [type] composition..." |
| Replace element | "Replace the [old] from the first image with the [new] from the second image" |

---

## Image Editing

### Adding/Removing Elements

Provide an image and describe changes. The model matches the original style, lighting, and perspective.

```
Add sunglasses to the person in this photo
Remove the background clutter behind the subject
Change the sky from overcast to a vibrant sunset
Replace the text on the sign with "GRAND OPENING"
```

### Inpainting (Semantic Masking)

Target specific parts of an image without a mask -- just describe what to change:

```
Using the provided image of a living room, change only the blue sofa
to a vintage brown leather chesterfield sofa. Keep everything else
exactly the same -- same lighting, same rug, same wall color.
```

### Style Transfer

```
Transform the provided photograph into the artistic style of Studio
Ghibli animation. Preserve the original composition and subject
positions but render everything with soft watercolor textures and
warm, saturated colors.
```

### Iterative Editing Strategy

1. Start with the original image and one clear edit
2. Review the result
3. Use the output as input for the next edit
4. One change at a time produces the best results

```
Round 1: "Make the lighting warmer, more golden hour"
Round 2: "Add slight film grain, Kodak Portra look"
Round 3: "Increase the background blur slightly"
```

---

## Prompt Templates by Use Case

### Photorealistic Product Shot

```
A high-resolution, studio-lit product photograph of [product] on a
[surface]. [Lighting setup] to [purpose]. Camera angle is [angle] to
showcase [feature]. Sharp focus on [detail area], soft background.
Shot on [camera] with [lens] at [aperture]. [Aspect ratio].
```

### UGC / Customer Review Photo

```
A [person description] using [product from reference image] in
[setting]. [Time of day] lighting, [environment details]. Realistic,
taken with an iPhone. The photo looks like it was snapped by a friend
standing nearby. Natural, unposed, authentic customer photo feel.
Slightly imperfect framing.
```

### Professional Headshot

```
A professional headshot of [person/reference] against a [background].
Warm, diffused studio lighting with a subtle hair light. Natural
expression, slight genuine smile. Shot on Canon EOS R5 with 85mm
f/2.0 lens. Soft creamy bokeh background. Natural skin texture.
```

### E-Commerce / Marketing

```
A professional e-commerce photograph of [product] on a [background].
[Lighting details]. Include the text "[headline]" in [font style] at
the [position]. [Aspect ratio and resolution].
```

### Logo with Text

```
Create a modern, minimalist logo for [brand] with the text "[text]"
in a [font style]. The design should be [style], with a [color scheme].
Clean vector style, centered composition.
```

### Minimalist / Negative Space (for text overlay)

```
A minimalist composition featuring a single [subject] positioned in
the [position] of the frame. The background is a vast, empty [color]
canvas, creating significant negative space for text overlay.
[Lighting]. [Aspect ratio].
```

### Infographic / Diagram

```
Create a vibrant infographic that explains [topic]. Show [elements]
and [relationships]. The style should be [style], suitable for
[audience]. Clear hierarchy, readable text.
```

---

## Configuration Options

### Aspect Ratios

`"1:1"` | `"3:4"` | `"4:3"` | `"9:16"` | `"16:9"`

Additional ratios supported by some models: `"2:3"`, `"3:2"`, `"4:5"`, `"5:4"`, `"21:9"`

### Resolutions (Nano Banana Pro only)

| Setting | Resolution | Notes |
|---|---|---|
| `"1K"` | ~1024x1024 | Default, fastest |
| `"2K"` | ~2048x2048 | Good balance of quality and speed |
| `"4K"` | ~4096x4096 | Highest quality, slowest |

**Important:** Resolution values MUST use uppercase K (`"2K"` not `"2k"`).

### Model Selection

| When to Use | Model |
|---|---|
| Final assets, text rendering, complex scenes | `gemini-3-pro-image-preview` (Pro) |
| Rapid iteration, drafts, exploring ideas | `gemini-2.5-flash-preview-05-20` (Flash) |
| Testing, simple generation, free tier | `gemini-2.0-flash-exp` (Fallback) |

**Recommended workflow:** Draft with Flash (fast, cheap) -> Finalize with Pro (slow, high quality).

---

## Batch Generation Workflow

When generating multiple images (galleries, review photos, marketing variants):

### Step 1: Prepare output directory

```bash
mkdir -p ./output/product-photos
```

### Step 2: Generate sequentially with the MCP tool

Each call to `generate_image` includes the same product reference and a unique prompt/output path:

```
Generate 1: Outdoor use scene -> ./output/product-photos/outdoor.png
Generate 2: Kitchen counter scene -> ./output/product-photos/kitchen.png
Generate 3: Close-up detail shot -> ./output/product-photos/detail.png
Generate 4: Customer review style -> ./output/product-photos/review.png
```

### Step 3: Optimize for web

Generated images are large (7-9 MB per JPG). For web use, compress them:

```bash
# Using sharp CLI
npx sharp-cli -i ./output/product-photos/*.png -o ./output/optimized/ --quality 80

# Or rely on Next.js Image component for automatic optimization at serve time
```

### File Size Warning

Do NOT serve raw generated images directly on the web -- they will destroy page load performance. Always optimize or use a framework that handles it automatically (Next.js `Image`, Astro image optimization, etc.).

---

## Background Removal with rembg

`rembg` is a local CLI tool for removing image backgrounds. Pairs well with the MCP server.

### Basic Usage

```bash
# Single file
rembg i input.jpg output.png

# Best quality model for product photos
rembg i -m birefnet-general input.jpg output.png

# Batch process a folder
rembg p ./input-folder ./output-folder
```

### Available Models

| Model | Best For |
|---|---|
| `u2net` | General purpose (default) |
| `birefnet-general` | Best overall quality |
| `bria-rmbg` | State-of-the-art background removal |
| `u2net_human_seg` | Human/portrait photos |
| `birefnet-portrait` | Portrait-specific |

### Combined Workflow

1. **rembg** to remove backgrounds from product photos -> transparent PNGs
2. **`edit_image`** to place products in new scenes or add branding
3. **`generate_image`** with reference images to create hero backgrounds, lifestyle shots, marketing assets

---

## Limitations & Best Practices

### Current Limitations

- **Text fidelity** -- Small text, fine details, and spelling may not be perfect (Pro is much better than Flash)
- **Factual accuracy** -- Always verify data in generated visuals (diagrams, infographics, charts)
- **Translation** -- Multilingual text rendering may have grammar issues
- **Complex edits** -- Blending and lighting changes across multiple elements can produce artifacts
- **Character consistency** -- Usually reliable with reference images but can drift across many edits
- **File sizes** -- Generated images are 7-9 MB per file -- must be optimized for web delivery
- **Speed** -- Pro model takes 10-30+ seconds per image; plan accordingly for batch work

### Best Practices

1. **Start simple, iterate** -- Even 1-2 sentences can produce good results. Add detail as needed rather than front-loading everything.
2. **One edit at a time** -- For multi-turn editing, change one variable per iteration for predictable results.
3. **Be specific about text** -- Wrap exact text in quotes: `the text "HELLO WORLD"`.
4. **State what to keep** -- When editing, explicitly say "keep everything else unchanged."
5. **Use photography language** -- Specific camera terms (bokeh, golden hour, f/1.8, rim lighting) produce better results than vague adjectives.
6. **Reference images by ordinal position** -- "the first image", "the second image", not "image 1" or "image A".
7. **Always specify outputPath** -- So files save directly where you need them.
8. **Always pass product reference images** -- For lifestyle shots, always include the actual product photo so the model doesn't hallucinate the product's appearance.
9. **Draft with Flash, finalize with Pro** -- Use the fast model for iteration and the pro model for final assets.
10. **Use "realistic, taken with an iPhone"** -- For UGC/review style photos, this single phrase dramatically shifts output toward authentic customer-style photography.
11. **Describe the photographer's POV** -- "snapped by a friend", "taken from across the room" -- this grounds composition in a believable perspective and avoids the overly polished AI look.
12. **Describe the scene narratively** -- A flowing paragraph produces more coherent images than a keyword list. Write prompts like you're describing a photograph to someone who can't see it.
13. **Request imperfections for realism** -- Natural skin pores, flyaway hairs, worn materials, chipped paint. Perfection is the hallmark of AI-generated images.
14. **Reference film stocks** -- "Kodak Portra 400 color grading" or "shot on a Leica M6" adds organic, analog character that fights the digital AI look.
