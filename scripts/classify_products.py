#!/usr/bin/env python3
"""First-pass product_type classifier for My Toy Wagon.

Reads the bulk product export (JSONL, products with nested collections) and
proposes a canonical product_type for each product using, in priority order:
already-canonical, the Nanchen brand rule, title keywords, collection
membership, brand defaults, then a small-world fallback. Outputs a review CSV.
Nothing is written to Shopify here.
"""
import json, csv

SRC = "_work/products.jsonl"
OUT = "_work/classification.csv"

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

TITLE_RULES = [
    ("Puzzles", ["puzzle","jigsaw"]),
    ("Marble & Ball Runs", ["marble run","ball run","ball track","marble tree","marble tower","ball drop"]),
    ("Magnetic Tiles", ["magnetic tile","magna-tile","magnatile","magna tile","connetix","magnetic building"]),
    ("Stacking & Sorting", ["stacker","stacking","shape sorter","sorting","ring stack","nesting"]),
    ("Teethers", ["teether","teething"]),
    ("Loveys", ["lovey","lovie","comforter","blanket doll","nuckel","schmusetuch","cuddle cloth","security blanket","snuggler"]),
    ("Rattles & Grasping Toys", ["rattle","grasping","clutching"]),
    ("Puppets", ["puppet"]),
    ("Play Dough & Tools", ["play dough","playdough","play-dough","dough cutter","dough tool","modelling beeswax","modeling beeswax","eco cutter","eco-cutter","cookie cutter","biscuit cutter"]),
    ("Painting & Drawing", ["crayon","watercolor","watercolour"," paint","paints","painting","chalk","coloring","colouring"," marker","easel","drawing","doodle","sketch","pastels"]),
    ("Other Crafts", ["stamp","craft kit","felting kit","weaving","sewing kit","needle felt","knitting"," loom","sticker"]),
    ("Ornaments & Stockings", ["ornament","stocking","advent","bauble"]),
    ("Garlands & Bunting", ["garland","bunting","wreath","pennant"]),
    ("Lighting", ["night light","nightlight","night-light"," lamp","lantern","fairy lights","wall light"]),
    ("Playsilks", ["playsilk","play silk","play-silk","silk cloth","wondercloth","canopy silk"]),
    ("Mobiles", ["mobile"]),
    ("Baskets & Storage", ["basket","storage bin","toy bin","hamper"]),
    ("Blankets & Swaddles", ["swaddle","baby blanket"," blanket"," quilt","duvet"]),
    ("Musical Instruments", ["guitar","xylophone"," drum","piano","kalimba","glockenspiel","tambourine","maraca","ukulele","harmonica","castanet","rainmaker"," flute","whistle"]),
    ("Books", [" book","board book","picture book","storybook"]),
    ("Waldorf Birthday", ["birthday crown","birthday ring","birthday garland","celebration ring"]),
    ("Dress-ups & Costumes", ["costume","dress up","dress-up","dressup"," wand","magic wand","sword","shield"," cape"," wings","fairy wings"," mask","tutu"," crown"," tiara","apron","superhero"]),
    ("Tents & Teepees", ["teepee","tipi"," tent","play tent","canopy"]),
    ("Riding & Climbing Toys", ["scooter","balance bike","tricycle"," trike","ride-on","ride on","rocker","hobby horse","wagon","pikler","climbing","balance board","wobble board","see saw","seesaw","push bike"]),
    ("Sand & Water Play", ["sand toy","beach toy","water play","sand mold","pool toy"]),
    ("Bath Play", ["bath toy","bath time","bath book"]),
    ("Toy Vehicles", [" car ","truck","train","vehicle","digger","excavator"," plane","airplane"," boat"," tractor","camper","bulldozer","fire engine","locomotive","racer"]),
    ("Play Food", ["play food","felt food","wooden food","grocer","play cake","ice cream set"]),
    ("Kitchen & House Play", ["kitchen","tea set","teapot","tea cup","cookware","pots and pans","cleaning set","market stand","cash register","baking set"]),
    ("Dollhouses", ["dollhouse","doll house","dolls house"]),
    ("Woodland Homes & Fairy Houses", ["tree house","treehouse","fairy house","fairy castle","fairy door","mushroom house","gnome home"," castle","village set","fairy garden"]),
    ("Trees & Landscapes", [" tree","trees"," shrub"," bush"," forest"," hedge","landscape","nature table","stump","toadstool"]),
    ("Fairies & Gnomes", ["gnome","fairy","pixie"," elf","peg doll","peg people","flower child","root child","tomte"]),
    ("Stuffed Animals", ["stuffed animal","plush","soft toy","cuddly toy","softie","stuffie"]),
    ("Counting, Numbers & Letters", ["counting","abacus","number","alphabet","letters"," math","spelling","phonics"]),
    ("Building Blocks", ["building block","wooden block","block set"," blocks","unit block","arch block","brick set"]),
    ("Dolls", ["doll"]),
    ("Cloth & First Books", ["cloth book","soft book","fabric book","quiet book"]),
    ("Push & Pull-Along", ["pull along","pull-along","push along","push toy","pull toy","walker"]),
    ("Games", ["board game","memory game","matching game","domino","card game","skittles","bowling","ring toss"]),
]

# Clean category collections, most specific first. First membership hit wins.
COLLECTION_PRIORITY = [
    ("marble-and-ball-runs","Marble & Ball Runs"),
    ("magnetic-tiles","Magnetic Tiles"),("connetix","Magnetic Tiles"),("magnetic-play","Magnetic Tiles"),
    ("teethers-and-clutching-toys","Teethers"),
    ("rattles","Rattles & Grasping Toys"),("grasping-toys-1","Rattles & Grasping Toys"),
    ("mobiles","Mobiles"),
    ("puppet-sets","Puppets"),
    ("dough-cutters","Play Dough & Tools"),("eco-cutter™","Play Dough & Tools"),("play-dough-and-accessories","Play Dough & Tools"),("land-of-dough","Play Dough & Tools"),
    ("crayons","Painting & Drawing"),("paints","Painting & Drawing"),("crayon-rocks","Painting & Drawing"),("doodling","Painting & Drawing"),("easel","Painting & Drawing"),("wooden-art-easels","Painting & Drawing"),
    ("hobby-horse-collection","Riding & Climbing Toys"),("ride-on-toys-and-accessories","Riding & Climbing Toys"),("scooters","Riding & Climbing Toys"),
    ("tents-and-teepees","Tents & Teepees"),
    ("ornaments-and-stockings","Ornaments & Stockings"),
    ("garlands_and_wreaths","Garlands & Bunting"),
    ("bolga-baskets","Baskets & Storage"),("desert-rose-baskets","Baskets & Storage"),("baskets","Baskets & Storage"),
    ("little-lights","Lighting"),
    ("soft-and-quiet-books","Cloth & First Books"),
    ("wall-decor-artwork-banners-decals-posters-prints-and-hangings","Wall Decor"),
    ("counting-and-math-toys","Counting, Numbers & Letters"),("alphabet-toys","Counting, Numbers & Letters"),("learning-cards-and-tiles","Counting, Numbers & Letters"),
    ("waldorf-crowns","Waldorf Birthday"),
    ("costumes-and-dress-up","Dress-ups & Costumes"),("dress-up-and-costumes","Dress-ups & Costumes"),
    ("woodland-homes-and-fairy-houses","Woodland Homes & Fairy Houses"),("houses-buildings-and-towns","Woodland Homes & Fairy Houses"),("treehouses-and-accessories","Woodland Homes & Fairy Houses"),
    ("trees-and-more-trees","Trees & Landscapes"),
    ("model-cars","Toy Vehicles"),("wooden-transportation-toys","Toy Vehicles"),
    ("puzzle-michele-wilson","Puzzles"),("puzzles","Puzzles"),
    ("stacking-toys","Stacking & Sorting"),
    ("play-food","Play Food"),
    ("kitchenware","Kitchen & House Play"),("kitchen-play","Kitchen & House Play"),
    ("cuddly-toys","Stuffed Animals"),
    ("ambrosius-fairies","Fairies & Gnomes"),("painted-peg-dolls","Fairies & Gnomes"),("gnomes-fairies-princes-peg-dolls","Fairies & Gnomes"),("fairies-and-gnomes","Fairies & Gnomes"),
    ("dolls-and-accessories","Dolls"),
    ("wooden-animals","Wooden Animals"),
    ("musical-toys","Musical Instruments"),("loog-guitars","Musical Instruments"),
    ("sensory-discovery","Sensory & Loose Parts"),
    ("build-and-construct","Building Blocks"),
    ("felt-play-mats-and-playscapes","Small World Play"),("playscapes-fairy-houses-castles-playmats","Small World Play"),("small-world-play","Small World Play"),
]

BRAND_DEFAULT = {
    "Loog Guitars":"Musical Instruments","Loog":"Musical Instruments",
    "Connetix":"Magnetic Tiles","Connetix Tiles":"Magnetic Tiles",
    "Little Lights":"Lighting","Little Lights US":"Lighting",
    "Sarah's Silks":"Playsilks",
    "Candylab":"Toy Vehicles","Candylab Toys":"Toy Vehicles",
    "Eco-Cutter":"Play Dough & Tools","Eco Cutter":"Play Dough & Tools","Land of Dough":"Play Dough & Tools",
    "MesaSilla":"Kids Furniture","MesaSilla USA":"Kids Furniture","Milton & Goose":"Kids Furniture",
}
SMALLWORLD_BRANDS = {"Bumbu Toys","Holztiger","Grapat","Papoose Toys","Tara Treasures",
                     "Ambrosius","Fairyshadow","Brin d'Ours","Atelier des Peupliers"}

def classify(p, colls):
    title = (p.get("title") or "").lower()
    vendor = (p.get("vendor") or "").strip()
    cur = (p.get("productType") or "").strip()
    tags = [t.lower() for t in (p.get("tags") or [])]
    waldorf = "waldorf" in " ".join(tags) or "waldorf" in title

    if cur in CANON:
        return cur, "already canonical", "keep"
    if vendor.lower().startswith("nanchen"):
        if "rattle" in title: return "Rattles & Grasping Toys","nanchen+rattle","high"
        if any(k in title for k in ["blanket doll","comforter","nuckel"]): return "Loveys","nanchen+lovey","high"
        if "soft toy" in title: return "Stuffed Animals","nanchen+soft toy","high"
        return "Waldorf Dolls","nanchen default","high"
    for cat, kws in TITLE_RULES:
        for kw in kws:
            if kw in title:
                if cat == "Dolls" and waldorf:
                    return "Waldorf Dolls", f"title:{kw.strip()}+waldorf", "high"
                return cat, f"title:{kw.strip()}", "high"
    cset = colls.get(p["id"], set())
    for handle, cat in COLLECTION_PRIORITY:
        if handle in cset:
            conf = "low" if cat == "Small World Play" else "medium"
            return cat, f"collection:{handle}", conf
    if vendor in BRAND_DEFAULT:
        return BRAND_DEFAULT[vendor], f"brand:{vendor}", "medium"
    if vendor in SMALLWORLD_BRANDS:
        return "Small World Play", f"brand-fallback:{vendor}", "low"
    return "", "no match", "review"

def main():
    products = {}
    colls = {}
    with open(SRC) as f:
        for line in f:
            line=line.strip()
            if not line: continue
            o = json.loads(line)
            if "__parentId" in o:
                colls.setdefault(o["__parentId"], set()).add(o.get("handle"))
            else:
                products[o["id"]] = o
    rows=[]; conf_counts={"keep":0,"high":0,"medium":0,"low":0,"review":0}; cat_counts={}
    for pid,p in products.items():
        proposed,reason,conf = classify(p, colls)
        rows.append({"handle":p.get("handle",""),"title":p.get("title",""),"vendor":p.get("vendor",""),
                     "status":p.get("status",""),"current_type":p.get("productType",""),
                     "proposed_type":proposed,"reason":reason,"confidence":conf})
        conf_counts[conf]+=1
        if conf!="keep": cat_counts[proposed or "(none)"]=cat_counts.get(proposed or "(none)",0)+1
    with open(OUT,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=["handle","title","vendor","status","current_type","proposed_type","reason","confidence"])
        w.writeheader(); w.writerows(rows)
    flds=["handle","title","vendor","status","current_type","proposed_type","reason","confidence"]
    act=[r for r in rows if r["status"]=="ACTIVE"]
    with open("_work/classification_active.csv","w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=flds); w.writeheader(); w.writerows(act)
    with open("_work/active_review.csv","w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=flds); w.writeheader()
        w.writerows([r for r in act if r["confidence"] in ("low","review")])
    active = [r for r in rows if r["status"]=="ACTIVE"]
    a_conf={"keep":0,"high":0,"medium":0,"low":0,"review":0}
    for r in active: a_conf[r["confidence"]]+=1
    a_weak=[r for r in active if r["confidence"] in ("low","review")]
    print(f"Total products: {len(products)}  (ACTIVE: {len(active)}, DRAFT/other: {len(products)-len(active)})")
    print("ALL by confidence:", conf_counts)
    print("ACTIVE by confidence:", a_conf)
    print(f"ACTIVE weak group (low+review): {len(a_weak)}")
    aw={}
    for r in a_weak: aw[r['reason']]=aw.get(r['reason'],0)+1
    print("  ACTIVE weak by reason:")
    for reason,n in sorted(aw.items(), key=lambda x:-x[1])[:12]:
        print(f"    {n:5d}  {reason}")
    print("\nProposed categories (new assignments only, all statuses):")
    for cat,n in sorted(cat_counts.items(), key=lambda x:-x[1]):
        print(f"  {n:5d}  {cat}")

if __name__=="__main__":
    main()
