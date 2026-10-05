# Quest Portal dice formulas

Quest Portal stores dice formulas in `rollButton`, `modifierWidget`, and collection cells in both rich notes and ordinary character-sheet tabs. The public MCP has no tool that executes a roll. Its rich-text envelopes check formula fields structurally but do not prove that a formula resolves or behaves as intended, so author conservative canonical syntax and preserve unfamiliar existing formulas.

## Core syntax

- Dice: `NdS`, such as `2d6`; omit the count with `d20`. Uppercase `D` is accepted. Use `4dF` for Fate dice and `d%` for percentile dice.
- Arithmetic: `+`, `-`, `*`, `/`, `%`, `**`, parentheses, and unary minus.
- Comparisons: `<`, `<=`, `>`, `>=`, and numeric `=`.
- Functions: `floor(x)`, `ceil(x)`, `round(x)`, `abs(x)`, `min(x,y)`, `max(x,y)`, and `if(condition,whenTrue,whenFalse)`.
- Keep/drop: `k`, `kh`, `kl`, `d`, `dh`, and `dl`, with an optional count that defaults to one. Example: `4d6kh3`.
- Explode/reroll: `!`, `!!`, `!p`, `r`, and `ro`, optionally with a modifier target using only `<`, `>`, or `=`. Examples: `3d6!>4` and `2d8ro<2`.
- Success/failure and critical matching: comparison success tests, `f`, `cs`, and `cf`. Their modifier targets also accept only `<`, `>`, or `=`. Examples: `3d6>3f1` and `1d20cs>19cf1`.
- Match/sort: `m`, `mt`, `s`, `sa`, and `sd`.
- Groups: comma-separated expressions inside braces, such as `{4d6,3d8}kh1`.
- Labels and colors: `[Attack]` and `#red`. Put them after the canonical expression.
- Formula references: `@{id}` with an optional `[label]`, such as `@{str-mod}[Strength modifier]+1d20`. IDs use letters, digits, underscores, or hyphens.

A formula reference is meaningful only when the referenced formula link exists in the note's current formula graph and its dependency chain is valid. The public MCP does not resolve that graph for newly invented references. Preserve valid existing references; create one only when the exact target ID and relationship are known.

## Useful valid examples

| Formula                              | Intent                                            |
| ------------------------------------ | ------------------------------------------------- |
| `d20`                                | One d20                                           |
| `2d6+3`                              | Two d6 plus three                                 |
| `4dF`                                | Four Fate dice                                    |
| `d%`                                 | Percentile die                                    |
| `4d6kh3`                             | Roll four d6, keep highest three                  |
| `4d6dl1`                             | Roll four d6, drop lowest one                     |
| `2d8ro<2`                            | Reroll results below two once                     |
| `3d6!>4`                             | Explode results above four                        |
| `5d6!!`                              | Compound exploding d6 pool                        |
| `5d6!p`                              | Penetrating exploding d6 pool                     |
| `3d6>3f1`                            | Count successes above three and failures at one   |
| `1d20cs>19cf1`                       | Critical-success and critical-failure comparisons |
| `{4d6,3d8}kh1`                       | Keep the highest result from a group              |
| `floor((2d6+3)/2)`                   | Arithmetic with a supported function              |
| `if(1d20>=10,2d6,1d6)`               | Conditional result                                |
| `@{str-mod}[Strength modifier]+1d20` | Known formula reference plus a d20                |
| `1d20#red [Attack]`                  | Color and trailing label                          |

## Reject or repair these forms

These do not parse as complete supported formulas:

| Invalid      | Reason                              |
| ------------ | ----------------------------------- |
| `d`          | Missing sides                       |
| `attack`     | Label without an expression         |
| `(1d20`      | Unclosed parenthesis                |
| `min(1,2,3)` | `min` takes two arguments           |
| `if(1,2)`    | `if` takes three arguments          |
| `@{bad id}`  | Reference IDs cannot contain spaces |
| `@str`       | Reference requires braces           |
| `{1d6,}`     | Missing group expression            |
| `round()`    | Missing function argument           |
| `max(1)`     | Missing second argument             |

The parser intentionally treats remaining text after a valid expression as a label. As a result, parser acceptance alone is not proof of correctness: incomplete arithmetic, stray punctuation, JavaScript-like operators, or unsupported modifier operators can be swallowed or reinterpreted. In particular, do not author `1d6!>=6` or `1d20cs>=19`; `>=` and `<=` are valid only for whole-expression comparisons, not explode, reroll, success, failure, critical, or match targets. Also avoid forms such as `1d20 + `, `1d20)`, `1d20==10`, `1d20 && 2`, zero/negative-sided dice, duplicated dice operators, or arbitrary trailing words without `[label]`. Prefer the canonical examples above even if a noncanonical string happens to parse.
