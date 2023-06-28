import numpy as np


r_to_t_dict = {"no conv.": 0,   # Default
               "pt1000":   1,   # Pt1000 test (cal=MRDS3000-3006 ch3 V/mV T/0C
               "F":        11,  # F high low
               "G":        12,  # G high low
               "H":        13,  # H high low
               "N":        14,  # N high low     
               "L":        15,  # L high low
               "M":        16,  # M high low
               "RF100":    17,  # RF100 high low
               "MRDS":     18,  # MRDS
               "AR3":      19,  # AR3
               "a8":       20   # a8
               }


def r_to_t(conv):
    # Functions, I know that some functions occur multiple times,
    # but I wanted to stay as true as possible to Wim's program.

    def default(r):
        # case 0
        return r

    def pt1000test(r):
        # case 1
        return -280+np.exp(+15.96010078315383
                           -5.777265693615240*(np.log(r))
                           +1.719621878746819*(np.log(r))**2
                           -0.3296896904176034*(np.log(r))**3
                           +0.0325135160361472*(np.log(r))**4
                           -0.001238253183442626*(np.log(r))**5)

    def fhigh(r):
        # case 2
        return np.exp(16.01256220008178
                      -24.81483636871209*(np.log(r))
                      +17.32085139761442*(np.log(r))**2
                      -6.085430265212089*(np.log(r))**3
                      +1.173753050126549*(np.log(r))**4
                      -0.1183163650122031*(np.log(r))**5
                      +0.00491460677567561*(np.log(r))**6 )

    def spspecial(r):
        # case 3
        if r >= 7850:
            return np.exp(+42.32605191233305
                          -35.48617979865299*(np.log(1*(r)))
                          +15.6682358081070*(np.log(1*(r)))**2
                          -3.820230536108149*(np.log(1*(r)))**3
                          +0.5234443687473452*(np.log(1*(r)))**4
                          -0.0380286996197814*(np.log(1*(r)))**5
                          +0.001147509051044717*(np.log(1*(r)))**6)
        return ((np.log(r)-6.58231)/28.60582)**(-1/0.4712)

    def flow(r):
        # case 4
        return 1e-3*np.exp(-710.0262877572307
                           +322.9179399161088*(np.log(1000*r))
                           -58.45146855850959*(np.log(1000*r))**2
                           +5.326453045978480*(np.log(1000*r))**3
                           -0.2441816228296264*(np.log(1000*r))**4
                           +0.00451395822170572*(np.log(1000*r))**5 )

    def ghigh(r):
        # case 5
        return np.exp(29.58202363692958
                      -45.17177520349549*(np.log(r))
                      +29.88064676651070*(np.log(r))**2
                      -10.13755050845119*(np.log(r))**3
                      +1.89407235107920*(np.log(r))**4
                      -0.1852372231339097*(np.log(r))**5 
                      +0.00745225544312689*(np.log(r))**6)

    def glow(r):
        # case 6
        return 1e-3*np.exp(-544.5676017482177
                           +248.1849769707541*(np.log(1000*r))
                           -44.92493250442995*(np.log(1000*r))**2
                           +4.100831010357989*(np.log(1000*r))**3
                           -0.1885849850224576*(np.log(1000*r))**4
                           +0.00350331131792698*(np.log(1000*r))**5)

    def hhigh(r):
        # case 7
        return np.exp(37.63866172713826
                      -56.63260628198017*(np.log(r))
                      +36.44474795527592*(np.log(r))**2
                      -12.09994511601816*(np.log(r))**3
                      +2.217744387707139*(np.log(r))**4
                      -0.2131888447891270*(np.log(r))**5 
                      +0.00844030051139322*(np.log(r))**6 )

    def hlow(r):
        # case 8
        return 1e-3*np.exp(-649.6607257566526
                           +294.5907063066699*(np.log(1000*r))
                           -53.12596898007016*(np.log(1000*r))**2
                           +4.825044411084273*(np.log(1000*r))**3
                           -0.2205324289126790*(np.log(1000*r))**4
                           +0.00406648820879758*(np.log(1000*r))**5 )

    def nhigh(r):
        # case 9
        return np.exp(73.41324970439078
                      -106.3311032542545*(np.log(r))
                      +63.82555719639306*(np.log(r))**2
                      -19.92653500750758*(np.log(r))**3
                      +3.450043217733591*(np.log(r))**4
                      -0.3148258368795170*(np.log(r))**5 
                      +0.01188214232583087*(np.log(r))**6)

    def nlow(r):
        # case 10
        return 1e-3*np.exp(-1977.61071503373
                           +858.8345018658966*(np.log(1000*r))
                           -149.1881936568861*(np.log(1000*r))**2
                           +13.01167076142443*(np.log(1000*r))**3
                           -0.5697361944449233*(np.log(1000*r))**4
                           +0.01003208556390609*(np.log(1000*r))**5 )

    def fhighlow(r):
        # case 11
        if r >= 199.8:
            return np.exp(16.01256220008178
                          -24.81483636871209*(np.log(r))
                          +17.32085139761442*(np.log(r))**2
                          -6.085430265212089*(np.log(r))**3
                          +1.173753050126549*(np.log(r))**4
                          -0.1183163650122031*(np.log(r))**5
                          +0.00491460677567561*(np.log(r))**6 )
        return 1e-3*np.exp(-710.0262877572307
                           +322.9179399161088*(np.log(1000*r))
                           -58.45146855850959*(np.log(1000*r))**2
                           +5.326453045978480*(np.log(1000*r))**3
                           -0.2441816228296264*(np.log(1000*r))**4
                           +0.00451395822170572*(np.log(1000*r))**5 )

    def ghighlow(r):
        # case 12
        if r >= 204.7:
            return np.exp(29.58202363692958
                          -45.17177520349549*(np.log(r))
                          +29.88064676651070*(np.log(r))**2
                          -10.13755050845119*(np.log(r))**3
                          +1.89407235107920*(np.log(r))**4
                          -0.1852372231339097*(np.log(r))**5 
                          +0.00745225544312689*(np.log(r))**6)
        
        return 1e-3*np.exp(-544.5676017482177
                           +248.1849769707541*(np.log(1000*r))
                           -44.92493250442995*(np.log(1000*r))**2
                           +4.100831010357989*(np.log(1000*r))**3
                           -0.1885849850224576*(np.log(1000*r))**4
                           +0.00350331131792698*(np.log(1000*r))**5)
    
    def hhighlow(r):
        # case 13
        if r >= 212.79:
            return np.exp(37.63866172713826
                          -56.63260628198017*(np.log(r))
                          +36.44474795527592*(np.log(r))**2
                          -12.09994511601816*(np.log(r))**3
                          +2.217744387707139*(np.log(r))**4
                          -0.2131888447891270*(np.log(r))**5 
                          +0.00844030051139322*(np.log(r))**6 )
        return 1e-3*np.exp(-649.6607257566526
                           +294.5907063066699*(np.log(1000*r))
                           -53.12596898007016*(np.log(1000*r))**2
                           +4.825044411084273*(np.log(1000*r))**3
                           -0.2205324289126790*(np.log(1000*r))**4
                           +0.00406648820879758*(np.log(1000*r))**5 )

    def nhighlow(r):
        # case 14, Mixing Chamber YETI
        if r >= 225.524:
            # N high
            return np.exp(73.41324970439078
                          -106.3311032542545*(np.log(r))
                          +63.82555719639306*(np.log(r))**2
                          -19.92653500750758*(np.log(r))**3
                          +3.450043217733591*(np.log(r))**4
                          -0.3148258368795170*(np.log(r))**5 
                          +0.01188214232583087*(np.log(r))**6)
        # N low bias correction
        return 1E-3*np.exp(-1977.61071503373
                           +858.8345018658966*(np.log(1000*r))
                           -149.1881936568861*(np.log(1000*r))**2
                           +13.01167076142443*(np.log(1000*r))**3
                           -0.5697361944449233*(np.log(1000*r))**4
                           +0.01003208556390609*(np.log(1000*r))**5)

    def lhighlow(r):
        # case 15
        if r >= 223.76:
            # L high
            return np.exp(104.6750874814212
                          -148.3086471863297*(np.log(r))
                          +86.47846539832611*(np.log(r))**2
                          -26.30376527679790*(np.log(r))**3
                          +4.444252174117409*(np.log(r))**4
                          -0.3965138967120258*(np.log(r))**5
                          +0.01465514055121579*(np.log(r))**6 )
        # L low with bias correction
        return np.exp(-5.943338267631620
                      +6.244093734707140*(np.log(r-5.2))
                      -2.011598936020319*(np.log(r-5.2))**2
                      +0.3927201152433503*(np.log(r-5.2))**3
                      -0.0419866882804895*(np.log(r-5.2))**4
                      +0.002200681550971356*(np.log(r-5.2))**5)

    def mhighlow(r):
        # case 16
        if r >= 234.19:
            # M high
            return np.exp(252.7479592137451
                          -335.5111793651910*(np.log(r))
                          +184.2587231397065*(np.log(r))**2
                          -53.31965387121053*(np.log(r))**3
                          +8.607951369319844*(np.log(r))**4
                          -0.7358641617817465*(np.log(r))**5
                          +0.02607920087098386*(np.log(r))**6)
        # M low bias correction
        return 1E-3*np.exp(-1481.063886828427
                           +632.4460811462583*(np.log(1000*r))
                           -108.2946175749663*(np.log(1000*r))**2
                           +9.345244793972663*(np.log(1000*r))**3
                           -0.4063608406993035*(np.log(1000*r))**4
                           +0.00713527326482104*(np.log(1000*r))**5)

    def RF100highlow(r):
        # case 17
        if r >= 90:
            # RF100 high
            return np.exp(+93.676905857752
                          -217.342944180393*(np.log(r*0.1))
                          +189.113889383055*(np.log(r*0.1))**2
                          -81.142864499611*(np.log(r*0.1))**3
                          +18.635568586572*(np.log(r*0.1))**4
                          -2.201508223114*(np.log(r*0.1))**5 
                          +0.105386314079*(np.log(r*0.1))**6)
        # RF100 low
        return np.exp(-466.296008848081
                      +784.495465820407*(np.log(r*0.1))
                      -496.814648787330*(np.log(r*0.1))**2
                      +140.391660314194*(np.log(r*0.1))**3
                      -14.857438050347*(np.log(r*0.1))**4)

    def MRDS(r):
        # case 18
        return 102073/(r-5.38)

    def AR3(r):
        # case 19
        return np.exp(-16.985738592265
                      +20.869593118260*(np.log(r))
                      -9.403401237195*(np.log(r))**2
                      +2.210818028415*(np.log(r))**3
                      -0.260713605058*(np.log(r))**4
                      +0.012529791664*(np.log(r))**5)

    def A8(r):
        # case 20
        return np.exp(-34.124813158161
                      +38.543806856537*(np.log(r))
                      -16.635982614833*(np.log(r))**2
                      +3.672767013032*(np.log(r))**3
                      -0.406705361858*(np.log(r))**4
                      +0.018288321417*(np.log(r))**5)

    return {0: default,         # Default
            1: pt1000test,      # Pt1000 test (cal=MRDS3000-3006 ch3 V/mV T/0C
            2: fhigh,           # F  high
            3: spspecial,       # SP special
            4: flow,            # F low
            5: ghigh,           # G high
            6: glow,            # G low
            7: hhigh,           # H high
            8: hlow,            # H low
            9: nhigh,           # N high
            10: nlow,           # N low
            11: fhighlow,       # F high low
            12: ghighlow,       # G high low
            13: hhighlow,       # H high low
            14: nhighlow,       # N high low     
            15: lhighlow,       # L high low
            16: mhighlow,       # M high low
            17: RF100highlow,   # RF100 high low
            18: MRDS,           # MRDS
            19: AR3,            # AR3
            20: A8              # a8
            }.get(conv, 0)


if __name__ == "__main__":
    print("Just copy the function and use it in your code")