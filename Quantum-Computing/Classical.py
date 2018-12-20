class Adder():
    def __init__(self):
        pass
    
    
    def define_characters(self):
        '''Defines lines to draw logic circuits with'''
        V = '\u2502'
        H = '\u2500'
        DR = '\u2514'
        DL = '\u2518'
        RD = '\u2510'
        LD = '\u250c'
        UT = '\u252c'
        DT = '\u2534'
        RT = '\u2524'
        LT = '\u251c'
        return V,H,DR,DL,RD,LD,UT,DT,RT,LT
    
    
    def prepare_inputs(self,a,b):
        '''
        - Converts decimal numbers to binary
        - Converts binary numbers to strings
        - Adds zeros to the front of the shorter string to match the length of the longer string
        '''
        A = str(bin(a)[2:])
        B = str(bin(b)[2:])
        
        if len(A) < len(B):
            for i in range(len(B)-len(A)):
                A = '0' + A
                
        if len(B) < len(A):
            for i in range(len(A)-len(B)):
                B = '0' + B
        
        print('{:>10} = {}'.format(a,A),end='\r')
        print('\n{:>10} = {}'.format(b,B),end='\r')
        return A,B
        
    def demo(self):        
        A, B = self.prepare_inputs(10,12)
        V,H,DR,DL,RD,LD,UT,DT,RT,LT = self.define_characters()
        
        C = '' #out
        carry = '0' # carry
        print("===========example=============")
        
        for d in range(-1,-len(A)-1,-1):
            
            print(A[d]+ 5*' '+ B[d])
            print(V+'  +  '+V)
            print(DR+ 2*H+ UT+ 2*H+ DL)
            print(3*' '+V+' carry')
            print(3*' '+LT+7*H+RD)
            
            if A[d] == B[d] == '1': carry = '1'     
            else: carry = '0'
                
            print(3*' '+V+7*' '+V)
            
            if A[d] != B[d]: C = '1' + C
            elif A[d] == B[d]: C = '0' + C
                    
            print(3*' '+C[d]+7*' '+carry)
            print()
    
    
    def add(self, A,B):
        A, B = self.prepare_inputs(A,B)
        V,H,DR,DL,RD,LD,UT,DT,RT,LT = self.define_characters()
        
        C = '' #out
        carry = '0' # carry
        print('\n')
        for d in range(-1,-len(A)-1,-1):

            print(carry+ 5*' '+ A[d]+ 5*' '+ B[d])
            print(V+ '  +  '+    V+'  +  '+V)
            print(DR+ 5*H+ DT+ 2*H+ UT+ 2*H+  DL)
            print(6*' '+    3*' '+V)
            print(LD+ 8*H+ RT)   
            print(V+' carry  '+V)
            
            if (A[d] != B[d] and carry == '0') or (A[d] == B[d] == '0' and carry == '1') or (A[d] == B[d] == carry == '1'): 
                C = '1' + C
            else: C = '0' + C
                    
            print(V+7*' '+    '['+C[d]+']'+C[1:])
            
            if (A[d] == B[d] == '1') or (A[d] == carry == '1') or (B[d] == carry == '1'): 
                carry = '1'     
            else: carry = '0'
        
        if carry == '1':
            C = carry + C
            c = int(len(C)/2)
            print(V + 6*' ' + DR + (c+1)*H + UT + c*H + DL)
            print(carry + ' ' + 3*H +' ' + '['+carry+']'+ '['+C[1:]+']')
            print(5*' ' + DR + (c+2)*H + UT + (c+2)*H + DL)
            print(7*' ' + '['+C+']' + ' = ' + str(int(C,2)))
        elif carry == '0':
            c = int(len(C)/2)
            print(V + 6*' ' + DR + (c+1)*H + UT + c*H + DL)
            print(carry + 8*' '+'['+C+']'+' = ' + str(int(C,2)))
      
