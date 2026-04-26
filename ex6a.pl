% Human-style: Use a clear entry point and catch input errors
calculator :-
    repeat,
    show_menu,
    read_input(Choice),
    (Choice == 5 -> writeln('Goodbye!'), ! ; handle_action(Choice), fail).

show_menu :-
    format('~n--- Prolog Calculator ---~n'),
    format('1. Add | 2. Sub | 3. Mul | 4. Div | 5. Exit~n'),
    write('Choice: ').

read_input(Val) :-
    catch(read(Val), _, (writeln('Invalid input!'), Val = 0)).

handle_action(Choice) :-
    member(Choice, [1,2,3,4]), !,
    write('First number: '), read(A),
    write('Second number: '), read(B),
    calculate(Choice, A, B).
handle_action(_) :- writeln('Please select 1-5.').

calculate(1, A, B) :- Res is A + B, format('Result: ~w~n', [Res]).
calculate(2, A, B) :- Res is A - B, format('Result: ~w~n', [Res]).
calculate(3, A, B) :- Res is A * B, format('Result: ~w~n', [Res]).
calculate(4, _, 0) :- !, writeln('Error: Division by zero.').
calculate(4, A, B) :- Res is A / B, format('Result: ~w~n', [Res]).