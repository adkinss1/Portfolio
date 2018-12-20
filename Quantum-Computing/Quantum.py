class Adder():
    def __init__(self):
        pass
    
    def define_characters(self):
        '''Defines lines to draw registers with'''
        V = '\u2502'
        H = '\u2500'
        Cb = '\u25A0'
        X = '\u253C'
        return V,H,Cb,X
    
    
    def X(self, target):
        if target == '0':
            return '1'
        if target == '1':
            return '0'
    
    def CX(self, target, c_1):
        if c_1 == '0':
            return target
        if c_1 == '1':
            return self.X(target)
    
    def CCX(self, target, c_1, c_2):
        if c_2 == '0':
            return target
        if c_2 == '1':
            return self.CX(target, c_1)
    
    
    
    def prepare_inputs(self,a,b):
        '''
        - Converts decimal numbers to binary
        - Converts binary numbers to lists
        - Adds zeros to the front of the shorter list to match the length of the longer string
        '''
        A = bin(a)[2:] # strings
        B = bin(b)[2:]
        
        if len(A) < len(B):
            for i in range(len(B)-len(A)):
                A = '0' + A 
        if len(B) < len(A):
            for i in range(len(A)-len(B)):
                B = '0' + B
        
        A = [i for i in A] # list of digit strings
        B = [i for i in B]
        return A,B
        
    def setup(self):
        V,H,Cb,X = self.define_characters()
        
        Out = '' #out
        carry = '0' # carry

        print('C-in','A  ','B ','C-out')
        print('',V,' ',V,' ',V,' ',V)
        
        print('',V,' ',Cb+3*H+Cb+2*H+'[ ]')
        print('',V,' ',V,' ',V,' ',V)
        print('',Cb+3*H+Cb+3*H+X+2*H+'[ ]' + '    Carry Circuit')
        print('',V,' ',V,' ',V,' ',V)
        print('',Cb+3*H+X+3*H+Cb+2*H+'[ ]')
        print('',V,' ',V,' ',V,' ',V)
        print('',V,' ',V,' ',V,' ',V)
        print('',V,' ',V,' ',V,' ',V)
        print('',Cb+3*H+X+2*H+'[ ]'+'  '+V)
        print('',V,' ',V,' ',V,' ',V + '    Adder Circuit')
        print('',V,' ',Cb+2*H+'[ ]'+'  '+V)
    
        print(8*' ',V,' ',V)
        print(6*' ','[[B]]',V,'  A  ','B ','C-out')
        print(12*' ',V,' ',V,' ',V,' ',V)
        print(12*' ',V,' ',Cb+3*H+Cb+2*H+'[ ]')
        print(12*' ',V,' ',V,' ',V,' ',V)
        print(12*' ',Cb+3*H+Cb+3*H+X+2*H+'[ ]' + '    Carry Circuit')
        print(12*' ',V,' ',V,' ',V,' ',V)
        print(12*' ',Cb+3*H+X+3*H+Cb+2*H+'[ ]')
        print(12*' ',V,' ',V,' ',V,' ',V)
        print(12*' ',V,' ',V,' ',V,' ',V)
        print(12*' ',V,' ',V,' ',V,' ',V)
        print(12*' ',Cb+3*H+X+2*H+'[ ]'+'  '+V)
        print(12*' ',V,' ',V,' ',V,' ',V + '    Adder Circuit')
        print(12*' ',V,' ',Cb+2*H+'[ ]'+'  '+V)
        
    
    def demo(self):        
        self.add(58, 44)
        
    def add_silent(self, A,B):
        A, B = self.prepare_inputs(A,B)
        
        Cout = '0' #out
        Cin = '0' # carry
        for d in range(-1,-len(A)-1,-1):
            Cout = '0' # reset carry out
            Cout = self.CCX(Cout, A[d], B[d]) # Carry circuit  
            Cout = self.CCX(Cout, Cin, A[d])
            Cout = self.CCX(Cout, Cin, B[d])
            B[d] = self.CX(B[d], Cin) # Adder circuit
            B[d] = self.CX(A[d], B[d])
            Cin = Cout # Carry out goes into next carry in
            
        B = ''.join(B) # to sting   
        B = Cout+B
        print('      '+B+' = '+str(int(B,2)))       
        
    def add(self, A,B):
        A, B = self.prepare_inputs(A,B)
        V,H,Cb,X = self.define_characters()
        
        print('{:>10} = {}'.format(int(''.join(A),2),''.join(A))) # show numbers
        print('{:>10} = {}'.format(int(''.join(B),2),''.join(B)))
        
        Cout = '0' #out
        Cin = '0' # carry
        
        print('\n')
        print('C-in','A  ','B ','C-out')
        for d in range(-1,-len(A)-1,-1):
            S1 = (12*abs(d)-12)*' ' # spacing for first line
            S = (12*abs(d)-11)*' ' # spacing for each line
            Cout = '0' # reset carry out
            print(S1+'['+Cin+']','['+A[d]+']','['+B[d]+']','[0]')
            print(S+V,' ',V,' ',V,' ',V)
            
            Cout = self.CCX(Cout, A[d], B[d])
            print(S+V,' ',Cb+3*H+Cb+2*H+'['+Cout+']')
            print(S+V,' ',V,' ',V,' ',V)
            
            Cout = self.CCX(Cout, Cin, A[d])
            print(S+Cb+3*H+Cb+3*H+X+2*H+'['+Cout+']'+ '    Carry Circuit')
            print(S+V,' ',V,' ',V,' ',V)
            
            Cout = self.CCX(Cout, Cin, B[d])
            print(S+Cb+3*H+X+3*H+Cb+2*H+'['+Cout+']')
            print(S+V,' ',V,' ',V,' ',V)
            print(S+V,' ',V,' ',V,' ',V)
            print(S+V,' ',V,' ',V,' ',V)
            B[d] = self.CX(B[d], Cin)
            print(S+Cb+3*H+X+2*H+'['+B[d]+']'+'  '+V)
            print(S+V,' ',V,' ',V,' ',V + '     Adder Circuit')
            
            B[d] = self.CX(A[d], B[d])
            print(S+V,' ',Cb+2*H+'['+B[d]+']'+'  '+V)
            
            
            print(S+8*' '+V,' ',V)
            print(S+6*' '+'[['+B[d]+']]',V,'  A  ','B ','C-out')  
            Cin = Cout # Carry out goes into next carry in
            
        B = ''.join(B) # to sting   
        print(S+11*' '+'['+Cout+']')
        print('C-out',' ','B')
        print(' ['+Cout+']'+'  '+'['+B+']')
        B = Cout+B
        print('      '+B+' = '+str(int(B,2)))