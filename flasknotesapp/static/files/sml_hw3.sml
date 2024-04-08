(* 
###################################################################################
Your name: Krishnavamsi Bommireddy

I affirm that I have not violated the
Academic Integrity policies detailed in the syllabus
###################################################################################
*)

(* #1 - duplist 
* Duplicates each element of a list.
* Utilizes foldr to iterate from the end of the list to the start, appending each element twice to the result list.
* The cons operator (::) ensures efficient list construction without full list traversal.
*)
fun duplist x = foldr (fn (a, b) => a :: a :: b) [] x;

(* #2 - mylength *)
(* 
 * Calculates the length of a list.
 * Uses foldl to traverse the list from start to end, incrementing a counter for each element.
 *)
fun mylength x = foldl (fn (a, b) => b + 1) 0 x;

(* #3 - il2absrl *)
(* Converts a list of integers to a list of their absolute values in real number form.
 * Each integer is first converted to its absolute value using abs function.
 * Then, it is implicitly converted to a real by multiplying with 1.0.
 *)
fun il2absrl x = map (fn a => real(abs a) * 1.0) x;

(* #4 - myimplode *)
(* 
 * Converts a list of characters to a single string.
 * Uses foldl to sequentially concatenate each character onto the accumulator string (`b`).
 * The `str` function converts each character to a string before concatenation.
 * Starts with an empty string ("") and accumulates the result by appending characters from left to right.
 *)
fun myimplode x = foldl (fn (a, b) => b ^ str a) "" x;

(* #5 - lconcat *)
(*
 * Concatenates a list of lists ('x') into a single list using foldl.
 * Iterates from the start to the end of the list 'x', accumulating the result by appending each sublist ('b') to the accumulator ('a').
 * Starts with an empty list ([]) as the initial accumulator, effectively flattening 'x' into a single list.
 *)
fun lconcat x = foldl (fn (a, b) => b @ a) [] x;

(* #6 - convert *)
(*
 * Splits a list of pairs into a pair of lists.
 * Uses foldr to iterate over the input list 'x' from the end to the beginning.
 * For each pair (a, b) in 'x', 'a' is prepended to the first list 'xs' and 'b' is prepended to the second list 'ys'.
 * Starts with a pair of empty lists ([], []) as the initial accumulator, ensuring elements are distributed accordingly.
 *)
fun convert x = foldr (fn ((a, b), (xs, ys)) => (a::xs, b::ys)) ([], []) x;


(* #7 - mymap *)
(*
 * Transforms each element of a list 'x' using a function 'f'.
 * Utilizes foldr to apply 'f' to each element ('a') from the end to the beginning of the list,
 * constructing a new list by prepending the transformed elements to the accumulator 'b'.
 * The process starts with an empty list ([]) and builds up the transformed list in the original element order.
 *)
fun mymap f x = foldr (fn (a, b) => f a :: b) [] x;

(* #8 - myfoldl *)
(*
 * Implements a custom fold-left operation.
 * 'f' is the accumulator function, applied to each element ('first') and the current accumulator ('init').
 * Iteration proceeds from the start (left) of the list to the end (right), updating 'init' with each element's contribution.
 * For an empty list, returns the initial accumulator 'init' directly.
 * For a non-empty list ('first::rest'), recursively applies 'f' to the head and the result of folding the rest.
 *)
fun myfoldl f init nil = init
| myfoldl f init (first::rest) = myfoldl f (f(first, init)) rest;

(* #9 - sumSome *)
(*
 * Sums elements of a list based on a predicate function 'f'.
 * 'f' determines whether an element should be included in the sum.
 * Iterates through the list: if 'f' applied to an element ('first') returns true, that element is added to the sum.
 * Otherwise, the element is skipped. The process is recursive, starting from the first element to the last.
 * Returns the total sum of elements for which 'f' returns true. For an empty list, the sum is 0.
 *)
fun sumSome f nil = 0 
| sumSome f (first::rest) =  if f first then first + sumSome f rest 
  else sumSome f rest;



fun count (item, list) = foldl (fn(a,b) => if a = item then b+1 else b) 0 list;


