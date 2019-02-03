* I find it delightful that the same group of people who pride themselves on dispassionate logic are also the ones who can’t resist emotionally-loaded terms for their work: “pure”, “side effect”, “lazy”, “persistent”, “first-class”, “higher-order”.
* Like most C-derived languages, assignment is an expression and not a statement.In some other languages, like Pascal, Python, and Go, assignment is a statement.
* "Lexical" comes from the Greek "lexikos" which means "related to words". When we
use it in programming languages, it usually means a thing you can figure out
from source code itself without having to execute anything.
* Lexical scope came onto the scene with ALGOL. Earlier languages were often
dynamically scoped. They believed dynamic scope was faster to execute. Today,
thanks to early Scheme hackers, we know that isn't true. If anything, it's the
opposite.
* Dynamic scope for variables lives on some corners. Emacs Lisp defaults to
dynamic scope for variables. The [`binding`][binding] macro in Clojure provides
it. The widely-disliked [`with` statement][with] in JavaScript turns properties
on an object into dynamically-scoped variables.

[binding]: http://clojuredocs.org/clojure.core/binding
[with]: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/with
