# Veröffentlichung

| Teil | Wo | Quelle im Projekt |
|---|---|---|
| Fensterdekoration (C++) + Anwendungsstil (C++) | AUR: `haiku-plasma-theme-plugins` | `aur/haiku-plasma-theme-plugins/` |
| Globales Design, Plasma-Stil, Farbschema, Icons, Zeiger, Aurorae-Dekoration | store.kde.org | `tools/build_store.sh` → `dist/store/` |
| Quelltext | GitHub `haiku-plasma-theme` | ganzes Projekt |

## Reihenfolge

1. **GitHub:** Repository `haiku-plasma-theme` anlegen, `tools/set_github_user.sh <name>` ausführen, alles pushen, Tag `v1.0.0` setzen.
2. **AUR:** in `aur/haiku-plasma-theme-plugins/` `updpkgsums`, `makepkg -si` (Test), `makepkg --printsrcinfo > .SRCINFO`, hochladen (Details in der README dort).
3. **Store – Einzelteile zuerst:** `tools/build_store.sh`, dann die Ordner `2-plasma-style` bis `6-aurorae` in `dist/store/` hochladen. Jeder Ordner enthält Datei, Screenshots und `BESCHREIBUNG.md` (Kategorie, Tags, Kurzbeschreibung, Beschreibung).
4. **Store – Globales Design zuletzt:** In `store/global-theme.md` die Platzhalter `STORE_LINK_…` durch die Links der Einzelteile ersetzen, `tools/build_store.sh` erneut ausführen und `1-global-theme` hochladen. Danach die Store-Links auch in den anderen Beschreibungen (`STORE_LINK_GLOBAL_THEME`) nachtragen.

Hinweis: Ein globales Design aus dem Store installiert nur sich selbst. Deshalb verweist seine Beschreibung auf alle Einzelteile und auf das AUR-Paket.
