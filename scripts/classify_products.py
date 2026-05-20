#!/usr/bin/env python3
"""First-pass product_type classifier for My Toy Wagon.

Reads the bulk product export (JSONL) and proposes a canonical product_type for
each product using title keywords, brand defaults, and the locked taxonomy.
Outputs a review CSV. Nothing is written to Shopify here.
"""
import json, csv, sys, re

SRC = "_work/products.jsonl"
OUT = "_work/classification.csv"

# Locked canonical categories (proposals must be one of these).
CANON = {
    "Building Blocks","Magnetic Tiles","Marble & Ball Runs","Stacking & Sorting",
    "Kitchen & House Play","Play Food","Stuffed Animals","Wooden Animals",
    "Toy Vehicles","Dress-ups & Costumes","Puppets",
    "Painting & Drawing","Play Dough & Tools","Other Crafts","Handwork",
    "Dolls","Doll Accessories","Dollhouses","Dollhouse Furniture & Room Sets",
    "Waldorf Dolls","Waldorf Home","Waldorf Birthday","Playsilks","Fairies & Gnomes",
    "Early Learning","Musical Instruments","STEM Toys","Counting, Numbers & Letters",
    "Rattles & Grasping Toys","Teethers","Loveys","Blankets & Swaddles","Mobiles",
    "Cloth & First Books","Plush Baby Toys","Push & Pull-Along","Bath Play",
    "Games","Puzzles","Books",
    "Outdoor Toys","Riding & Climbing Toys","Sand & Water Play","Tents & Teepees",
    "Small World Play","Trees & Landscapes","Small World Figures & People",
    "Woodland Homes & Fairy Houses",
    "Garlands & Bunting","Wall Decor","Lighting","Rugs","Baskets & Storage",
    "Growth Charts","Kids Furniture",
    "Ornaments & Stockings","Sensory & Loose Parts","Nature Play",
}

# Ordered title rules: (category, [keyword,...]). First hit wins. Most specific first.
TITLE_RULES = [
    ("Puzzles", ["puzzle","jigsaw"]),
    ("Marble & Ball Runs", ["marble run","ball run","ball track","marble tree","marble tower","ball drop"]),
    ("Magnetic Tiles", ["magnetic tile","magna-tile","magnatile","magna tile","connetix","magnetic building"]),
    ("Stacking & Sorting", ["stacker","stacking","shape sorter","sorting","ring stack","nesting"]),
    ("Teethers", ["teether","teething"]),
    ("Loveys", ["lovey","lovie","comforter","blanket doll","nuckel","schmusetuch","cuddle cloth","security blanket","snuggler"]),
    ("Rattles & Grasping Toys", ["rattle","grasping","clutching"]),
    ("Puppets", ["puppet"]),
    ("Play Dough & Tools", ["play dough","playdough","play-dough","dough cutter","dough tool","modelling beeswax","modeling beeswax","eco cutter","eco-cutter","cookie cutter","biscuit cutter","land of dough"]),
    ("Painting & Drawing", ["crayon","watercolor","watercolour"," paint","paints","painting","chalk","coloring","colouring","marker","easel","drawing","doodle","sketch","pastels"]),
    ("Other Crafts", ["stamp","craft kit","felting kit","weaving","sewing kit","needle felt","knitting","loom","beeswax sheet","sticker"]),
    ("Ornaments & Stockings", ["ornament","stocking","advent","bauble"]),
    ("Garlands & Bunting", ["garland","bunting","wreath","pennant"]),
    ("Lighting", ["night light","nightlight","night-light"," lamp","lantern","fairy lights","wall light"]),
    ("Playsilks", ["playsilk","play silk","play-silk","silk cloth","wondercloth","mulberry silk","canopy silk"]),
    ("Mobiles", ["mobile"]),
    ("Rugs", [" rug","play mat rug","round rug"]),
    ("Baskets & Storage", ["basket","storage bin","toy bin","hamper"]),
    ("Blankets & Swaddles", ["swaddle","baby blanket","blanket","quilt","duvet"]),
    ("Musical Instruments", ["guitar","xylophone"," drum","piano","kalimba","glockenspiel","tambourine","maraca","ukulele","harmonica","music maker","musical instrument","castanet","rainmaker","flute","whistle"]),
    ("Books", [" book","board book","picture book","storybook"]),
    ("Waldorf Birthday", ["birthday crown","birthday ring","birthday garland","birthday spiral","grimm","celebration ring"]),
    ("Dress-ups & Costumes", ["costume","dress up","dress-up","dressup"," wand","magic wand","sword","shield"," cape"," wings","fairy wings","mask","tutu","crown","tiara","apron","superhero"]),
    ("Tents & Teepees", ["teepee","tipi","tent","play tent","canopy","playhouse tent"]),
    ("Riding & Climbing Toys", ["scooter","balance bike","tricycle"," trike","ride-on","ride on","rocker","hobby horse","wagon","pikler","climbing","balance board","wobble board","see saw","seesaw","push bike"]),
    ("Sand & Water Play", ["sand toy","beach toy","water play","sand mold","bath boat","pool toy"]),
    ("Bath Play", ["bath toy","bath time","bath book"]),
    ("Toy Vehicles", [" car ","cars","truck","train","vehicle","digger","excavator"," plane","airplane"," boat"," tractor","camper","bulldozer","fire engine","locomotive","automobile","racer"]),
    ("Play Food", ["play food","pretend food","felt food","wooden food","grocer","fruit set","vegetable set","tea biscuit","play cake","ice cream set"]),
    ("Kitchen & House Play", ["kitchen","tea set","teapot","tea cup","cookware","pots and pans","cleaning set","market stand","grocery store","cash register","coffee","baking set","dish set","cutting food"]),
    ("Dollhouses", ["dollhouse","doll house","dolls house"]),
    ("Woodland Homes & Fairy Houses", ["tree house","treehouse","fairy house","fairy castle","fairy door","mushroom house","gnome home","castle","village set","fairy garden"]),
    ("Trees & Landscapes", [" tree","trees","shrub","bush"," forest"," hedge","landscape","nature table","stump","toadstool","mushroom"]),
    ("Fairies & Gnomes", ["gnome","fairy","pixie"," elf","peg doll","peg people","flower child","root child","tomte","nisse"]),
    ("Stuffed Animals", ["stuffed animal","plush","soft toy","cuddly toy","softie","stuffie"]),
    ("Wooden Animals", ["wooden animal","animal figure","farm animal","safari animal","woodland animal","ocean animal","dinosaur figure","figurine animal"]),
    ("Counting, Numbers & Letters", ["counting","abacus","number","alphabet","letters","math","spelling","phonics"]),
    ("Building Blocks", ["building block","wooden block","block set","blocks","unit block","arch block","brick set"]),
    ("Dolls", ["doll"]),
    ("Cloth & First Books", ["cloth book","soft book","fabric book","quiet book"]),
    ("Push & Pull-Along", ["pull along","pull-along","push along","push toy","pull toy","walker"]),
    ("Sensory & Loose Parts", ["loose parts","sensory","treasure basket","stacking stones","sorting bowls"]),
    ("Outdoor Toys", ["garden","outdoor","gardening","kite","bug catcher","bird house","watering can"]),
    ("Games", ["board game","memory game","matching game","domino","card game","skittles","bowling","ring toss"]),
]

# Brands that map cleanly to one category when no strong title rule fires.
BRAND_DEFAULT = {
    "Loog Guitars":"Musical Instruments",
    "Connetix":"Magnetic Tiles","Connetix Tiles":"Magnetic Tiles",
    "Little Lights":"Lighting","Little Lights US":"Lighting",
    "Sarah's Silks":"Playsilks",
    "Candylab":"Toy Vehicles","Candylab Toys":"Toy Vehicles",
    "Eco-Cutter":"Play Dough & Tools","Eco Cutter":"Play Dough & Tools",
    "Land of Dough":"Play Dough & Tools",
    "Loog":"Musical Instruments",
    "MesaSilla":"Kids Furniture","MesaSilla USA":"Kids Furniture",
    "Milton & Goose":"Kids Furniture",
}
# Brands that are predominantly small-world when nothing else matches.
SMALLWORLD_BRANDS = {"Bumbu Toys","Holztiger","Grapat","Papoose Toys","Tara Treasures",
                     "Ambrosius","Fairyshadow","Brin d'Ours","Atelier des Peupliers"}

def classify(p):
    title = (p.get("title") or "").lower()
    vendor = (p.get("vendor") or "").strip()
    cur = (p.get("productType") or "").strip()
    tags = [t.lower() for t in (p.get("tags") or [])]
    waldorf = "waldorf" in " ".join(tags) or "waldorf" in title

    if cur in CANON:
        return cur, "already canonical", "keep"

    # Nanchen special rule
    if vendor.lower().startswith("nanchen"):
        if "rattle" in title: return "Rattles & Grasping Toys","nanchen+rattle","high"
        if any(k in title for k in ["blanket doll","comforter","nuckel"]): return "Loveys","nanchen+lovey","high"
        if "soft toy" in title: return "Stuffed Animals","nanchen+soft toy","high"
        return "Waldorf Dolls","nanchen default","high"

    for cat, kws in TITLE_RULES:
        for kw in kws:
            if kw in title:
                # doll -> Waldorf Dolls when waldorf context
                if cat == "Dolls" and waldorf:
                    return "Waldorf Dolls", f"title:{kw.strip()}+waldorf", "high"
                return cat, f"title:{kw.strip()}", "high"

    if vendor in BRAND_DEFAULT:
        return BRAND_DEFAULT[vendor], f"brand:{vendor}", "medium"

    if vendor in SMALLWORLD_BRANDS:
        return "Small World Play", f"brand-fallback:{vendor}", "low"

    return "", "no match", "review"

def main():
    rows = []
    counts = {}
    conf_counts = {"keep":0,"high":0,"medium":0,"low":0,"review":0}
    with open(SRC) as f:
        for line in f:
            line=line.strip()
            if not line: continue
            p = json.loads(line)
            proposed, reason, conf = classify(p)
            rows.append({
                "handle": p.get("handle",""),
                "title": p.get("title",""),
                "vendor": p.get("vendor",""),
                "status": p.get("status",""),
                "current_type": p.get("productType",""),
                "proposed_type": proposed,
                "reason": reason,
                "confidence": conf,
            })
            conf_counts[conf]+=1
            if conf != "keep":
                counts[proposed or "(none)"] = counts.get(proposed or "(none)",0)+1
    with open(OUT,"w",newline="") as f:
        w = csv.DictWriter(f, fieldnames=["handle","title","vendor","status","current_type","proposed_type","reason","confidence"])
        w.writeheader(); w.writerows(rows)

    print(f"Total products: {len(rows)}")
    print("By confidence:", conf_counts)
    print("\nProposed categories (new assignments only):")
    for cat,n in sorted(counts.items(), key=lambda x:-x[1]):
        print(f"  {n:5d}  {cat}")

if __name__=="__main__":
    main()
