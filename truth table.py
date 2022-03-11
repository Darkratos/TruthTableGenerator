from tabulate import tabulate

def get_closing_parenthesis( expr = '', off = 0 ):
    sub_level = 0

    for i in range( off, len( expr ) ):
        c = expr[ i ]

        if c == '(':
            sub_level += 1
        elif c == ')':
            sub_level -= 1

            if sub_level == 0:
                return expr[ off : i + 1 ]

    return ''

def get_opening_parenthesis( expr = '', off = 0 ):
    sub_level = 0

    for i in range( off, -1, -1 ):
        c = expr[ i ]

        if c == '(':
            sub_level += 1

            if sub_level == 0:
                return expr[ i : off + 1 ]

        elif c == ')':
            sub_level -= 1

    return ''

# Gets the left and right arguments for an operator
def get_args_op( expr = '', off_op = 0 ):
    if expr[ off_op ] == '!':
        if expr[ off_op + 1 ] == '(':
            arg = get_closing_parenthesis( expr, off_op + 1 )
            return [ '!' + arg, arg ]
        else:
            return [ expr[ off_op : off_op + 2 ], expr[ off_op + 1 : off_op + 2 ] ]
    else:
        args = [ '', '' ]

        if expr[ off_op - 1 ] == ')':
            args[ 0 ] = get_opening_parenthesis( expr, off_op - 1 )
        else:
            args[ 0 ] = expr[ off_op - 1 : off_op ]

        if expr[ off_op + 1 ] == '(':
            args[ 1 ] = get_closing_parenthesis( expr, off_op + 1 ) 
        else:
            args[ 1 ] = expr[ off_op + 1 : off_op + 2 ]

    return args

def parse( expr = '', step = 0, arr = [] ):
    if expr == '':
        return []

    sub_expr = expr

    if step == 0:               # 0 = Original and parenthesis
        arr.append( expr )

        while True:             # Search '('
            off = sub_expr.find( '(' )

            if off == -1:
                break

            arr.append( get_closing_parenthesis( sub_expr, off ) )

            sub_expr = sub_expr[ off + 1:: ]
    elif step == 1:
        precedence = [ [ '-' ], [ '>' ], [ '|', '&' ], [ '!' ] ]

        for op in precedence:
            for i in range( len( sub_expr ) ):             # Search for the operation
                if sub_expr[ i ] in op:
                    if i == len( sub_expr ) - 1:
                        raise Exception( f"{op} found in the end of the expression" )
                    elif i == 0 and op[ 0 ] != '!':
                        raise Exception( f"{op} found at the end of the expression" )

                    args = get_args_op( sub_expr, i )

                    arr.append( args[ 0 ] )
                    arr.append( args[ 1 ] )
    else:
        # Remove useless parethesis
        for i in range( len( arr ) ):
            if arr[ i ][ 0 ] == '(' and len( get_closing_parenthesis( arr[ i ] ) ) == len( arr[ i ] ):
                arr[ i ] = arr[ i ][ 1 : -1 ] 

        # Remove duplicates
        arr = list( dict.fromkeys( arr ) )

        # Reverse it
        arr.reverse( )

        return arr

    return parse( expr, step + 1, arr )

def validate( expr = '' ):
    if expr.count( '(' ) != expr.count( ')' ):
        return ''

    return expr

def solve( expr = '' ):
    expr = expr.replace( '(V)', 'V' ).replace( '(F)', 'F' )

    if expr[ 0 ] == '!':
        return 'F' if expr[ 1 ] == 'V' else 'V'
    elif expr[ 1 ] == '&':
        return 'V' if expr[ 0 ] == 'V' and expr[ 2 ] == 'V' else 'F'
    elif expr[ 1 ] == '|':
        return 'V' if expr[ 0 ] == 'V' or expr[ 2 ] == 'V' else 'F'
    elif expr[ 1 ] == '>':
        return expr[ 2 ] if expr[ 0 ] == 'V' else 'V'
    elif expr[ 1 ] == '-':
        return 'V' if expr[ 0 ] == expr[ 2 ] else 'F'
    else:
        raise Exception( f'Unknown operator {expr[ 1 ]}' )

def main( ):
    # Example: '(P&Q)|((Q-P)&(!(!R)))'
    expr = input( 'Expression: ' )

    arr_exprs = parse( validate( expr ) )

    # Count predicates
    num_predicates = 0

    for e in arr_exprs:
        if len( e ) == 1:
            num_predicates += 1

    lines = [ [ 0 for x in range( len( arr_exprs ) ) ] for y in range( 2 ** num_predicates ) ]
    max_val = 2 ** num_predicates - 1

    for j in range( max_val, -1, -1 ):
        for i in range( len( arr_exprs ) ):
            if i < num_predicates:
                val = ( j >> ( num_predicates - i - 1 ) ) & 1
                lines[ max_val - j ][ i ] = 'V' if val else 'F'
            else:
                # Iterate the previous expressions and eval
                current_expr = arr_exprs[ i ]
                for k in range( i - 1, -1, -1 ):
                    current_expr = current_expr.replace( arr_exprs[ k ], 'V' if lines[ max_val - j ][ k ] == 'V' else 'F' )

                lines[ max_val - j ][ i ] = solve( current_expr )
                
    print( tabulate( lines, arr_exprs, 'orgtbl' ) )

if __name__ == '__main__':
    main( )