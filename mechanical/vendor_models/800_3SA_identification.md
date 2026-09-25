# Allen-Bradley 800 Type 3SA station

Reviewed 2026-09-25 against user photographs IMG_4172.JPG, IMG_4173.JPG and IMG_4174.JPG, the user's physical observations, and Allen-Bradley literature.

## Identification

High-confidence identification: **Allen-Bradley Bulletin 800, Type 3SA standard-duty FOR/REV/STOP pushbutton station**, a fixed surface-mounted control station. Later manufacturer literature uses **800S-3SA** for the corresponding standard-duty FOR/REV/STOP station. Exact mechanical interchangeability between the user's vintage unit and a later 800S-3SA has not been established.

The user's unit is marked `800 / 3SA`, with additional `BF45` and `L` markings. The two extra markings have not been decoded from manufacturer documentation. They do not establish a date or series revision in this review.

User observations: approximately 25.4 mm button caps; flush green FOR and REV buttons; extended red STOP; cast-aluminum enclosure; operators mounted directly in the cover; 600 V AC marking on the rear terminal assembly mounted to the base plate. Cap diameter alone is not a panel cutout specification.

## Manufacturer evidence

1. [Historical A-B Wiring Diagrams, Bulletin 705](https://support.rockwellautomation.com/cc/okcsFattachCustom/get/40118_6), printed page 28 / PDF page 3, explicitly identifies “Bulletin 800, Type 3SA (standard duty).” Saved as [800_Type3SA_historical_wiring.pdf](drawings/800_Type3SA_historical_wiring.pdf). This confirms that the observed marking need not contain an S after 800.
2. [A117-CA001A-EN-P, Bulletin 800S catalog excerpt](https://support.rockwellautomation.com/cc/okcsFattachCustom/get/61320_3), pages 10-223 through 10-226. Page 10-224 lists 800S-3SA for FOR/REV/STOP. Page 10-223 describes the contact mechanism in the cover, wiring terminals in the base, and spring contacts joining the assemblies. This is consistent with the user's separated cover/base photographs. Saved as [800S_Catalog_Reference.pdf](drawings/800S_Catalog_Reference.pdf).
3. [800S Repair Parts, Rockwell Knowledgebase Technote 22608](https://configurator.rockwellautomation.com/api/Doc/800S%20Repair%20Parts%205-14-2021.pdf), document dated 5/13/2021, pages 1–2. Lists 800S-3SA under NEMA Type 1 Surface Mount Pushbutton Stations with FOR/REV/STOP legends. Identifies cover F-22279, cover nameplate H-24287 and button caps 40193-032-02 (FOR) and 40193-032-03 (REV). These are literature references, not verified replacement recommendations for the vintage unit. Saved as [800S_Repair_Parts.pdf](drawings/800S_Repair_Parts.pdf).
4. [Publication 800-2.0, June 1989](https://literature.rockwellautomation.com/idc/groups/literature/documents/wd/800-wd001_-en-p.pdf), page 9, lists 800S-3SA as standard duty alongside different heavy-duty 800H and oiltight 800T station families. The various 800-letter families should not be treated as mechanically interchangeable.

## Modeling reference

The user has deferred modeling the actual station because it is outside the panel enclosure. These references remain available for later work. Manufacturer geometry has not been substituted for measurements.

The upper-right drawing on catalog page 10-226 visibly depicts FOR/REV/STOP in a surface enclosure. Its approximate envelope dimensions are 58.7 mm wide × 136.5 mm high × 56.4 mm deep, with an additional 3.2 mm STOP projection and 104.8 mm vertical mounting-hole spacing. These are comparison dimensions for the catalog illustration, not confirmed dimensions of this older unit. The upper-right and lower-left drawing captions appear transposed: the upper-right shows three buttons and an enclosure despite the two-unit flush caption, while the lower-left shows two buttons on a flush plate despite the three-unit surface caption. Use the illustrated geometry and physical measurements, not those captions alone.

The catalog identifies 800S-3SA as Type 1. It separately describes other Type 4 enclosures as die-cast aluminum. The user's observation of cast aluminum does not by itself establish a Type 4 enclosure rating. No enclosure-rating or exact production-date conclusion is made for the vintage unit.

The catalog's 800S-3SA identifier remains the cross-reference used in the current BOM/model manifest. No KiCad symbol IDs, terminal mapping, or electrical design were changed by this identification work.
