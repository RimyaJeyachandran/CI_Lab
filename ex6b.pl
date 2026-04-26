% Humanized Set Operations
% Use 'memberchk' for faster performance than 'is_member'
is_member(X, List) :- memberchk(X, List).

% Union: Using recursion but keeping it readable
set_union([], S2, S2).
set_union([H|T], S2, Res) :-
    memberchk(H, S2), !, set_union(T, S2, Res).
set_union([H|T], S2, [H|Res]) :-
    set_union(T, S2, Res).

% Intersection: A more concise filter approach
set_intersection([], _, []).
set_intersection([H|T], S2, [H|Rest]) :-
    memberchk(H, S2), !, set_intersection(T, S2, Rest).
set_intersection([_|T], S2, Rest) :-
    set_intersection(T, S2, Rest).

% Cardinality: Human-written Prolog often uses the built-in length/2, 
% but if writing from scratch, we use an accumulator for efficiency.
set_cardinality(List, Count) :- length(List, Count).