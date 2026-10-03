import warnings, traceback
warnings.filterwarnings('ignore')

try:
    from ai_modules.gemini_flash import generate_outline
    from ai_modules.gemini_pro import generate_story
    from ai_modules.image_generator import generate_image
    from ai_modules.layout_builder import build_comic_layout
    from ai_modules.exporters import save_pdf

    print('Step 1: Generating outline...')
    outline = generate_outline('Superman saves Metropolis', 'Superman', 'Metropolis', 'Heroic', 'American Comic')
    print(f'  OK - {len(outline)} panels')
    print(f'  Panel 1 keys: {list(outline[0].keys())}')
    print(f'  Panel 1 title: {outline[0].get("title")}')

    print('Step 2: Generating story...')
    stories = generate_story(outline)
    print(f'  OK - {len(stories)} panels')
    print(f'  Panel 1 keys: {list(stories[0].keys())}')
    print(f'  Has narration: {"narration" in stories[0]}')
    print(f'  Narration: {stories[0].get("narration","")[:80]}')

    print('Step 3: Generating 1 image (first panel only)...')
    img = generate_image(stories[0].get('image_prompt', 'Superman comic art'))
    print(f'  OK - {img}')

    print('Step 4: Building layout...')
    images = [img] * 5
    layout = build_comic_layout(images, stories)
    print(f'  OK - {len(layout)} panels')

    print('Step 5: Saving PDF...')
    pdf = save_pdf(layout)
    print(f'  OK - {pdf}')

    print()
    print('=== ALL STEPS PASSED ===')

except Exception as e:
    print(f'\n=== FAILED AT: {e} ===')
    traceback.print_exc()
