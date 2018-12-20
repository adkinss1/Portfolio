
syms L H depthratio g positive
syms x t w T R U(x)

L1 = depthratio*L; 
L2 = L;

h1 = depthratio*H; 
h2 = H;
h(x) = x*H/L;

c1 = sqrt(g*h1);
c2 = sqrt(g*h2);

u(x,t)  = U(x)*exp(1i*w*t);
u1(x,t) = T*exp(1i*w*(t + x/c1));
u2(x,t) = exp(1i*w*(t + x/c2)) + R*exp(1i*w*(t - x/c2));
%% 
% In the transition region over the linear slope, use |dsolve| to solve 
% the ODE for the Fourier transform $U$ of $u$.

wavePDE(x,t) = diff(u,t,t) - g*diff(h(x)*diff(u,x),x);
slopeODE(x) = wavePDE(x,0); 
U(x) = dsolve(slopeODE);
%% 
% The solution $U$ is a complicated expression involving Bessel functions. 
% It contains two arbitrary "constants" that depend on $\omega$.

Const = setdiff(symvar(U), sym([depthratio,g,H,L,x,w]))
%% 
% For any Fourier mode, the overall solution must be a continuously differentiable 
% function of $x$. Hence, the function values and the derivatives must match at 
% the seam points $L_1$ and $L_2$. This provides four linear equations for $T$, 
% $R$, and the two constants in $U$.

du1(x) = diff(u1(x,0),x);
du2(x) = diff(u2(x,0),x);
dU(x)  = diff(U(x),x);

eqs =  [ U(L1) == u1(L1,0), U(L2) == u2(L2,0),...
        dU(L1) == du1(L1), dU(L2) == du2(L2)];
unknowns = [Const(1),Const(2),R,T];
%% 
% Solve these equations. 

[Cvalue1, Cvalue2, R, T] = solve(eqs, unknowns);
%% 
% Substitute the results back into $R$, $T$, and $U$.

U(x) = subs(U(x), {Const(1),Const(2)}, {Cvalue1,Cvalue2});
%% 
% You cannot directly evaluate the solution for $\omega = 0$ because both 
% numerator and denominator of the corresponding expressions vanish. Instead, 
% find the low frequency limits of these expressions.

simplify(limit(U(x), w, 0)) 
simplify(limit(R, w, 0)) 
simplify(limit(T, w, 0))
%% 
% These limits are remarkably simple. They only depend on the ratio of the 
% depth values defining the slope.
%% Substitute Symbolic Parameters with Numeric Values
% For the following computations, use these numerical values for the symbolic 
% parameters.
% 
% * Gravitational acceleration: $g = 9.81\;m/sec^2$
% * Depth of the canal: $H = 1\;m$
% * Depth ratio between the shallow and the deep regions: $depthratio = 0.04$
% * Length of the slope region: $L = 2\;m$

g = 9.81;
L = 10;
H = 1;
depthratio = 0.04; 

h1 = depthratio*H;
h2 = H;

L1 = depthratio*L;
L2 = L; 

c1 = sqrt(g*h1);
c2 = sqrt(g*h2);
%% 
% Define the incoming soliton of amplitude $A$ traveling to the left with 
% constant speed $c_2$ in the deep water region.

A = 0.3;
soliton = @(x,t) A.*sech(sqrt(3/4*g*A/H)*(x/c2+t)).^2;
%% 
% Choose $Nt$ sample points for $t$. The time scale is chosen as a multiple 
% of the (temporal) width of the incoming soliton. Store the corresponding discretized 
% frequencies of the Fourier transform in $W$.

Nt =  64;
TimeScale = 40*sqrt(4/3*H/A/g);
W = [0, 1:Nt/2 - 1, -(Nt/2 - 1):-1]'*2*pi/TimeScale;
%% 
% Choose $Nx$ sample points in $x$ direction for each region. Create sample 
% points $X1$ for the shallow water region, $X2$ for the deep water region, and 
% $X12$ for the slope region.

Nx = 100;
x_min = L1 - 4;
x_max = L2 + 12;
X12 = linspace(L1, L2, Nx);
X1  = linspace(x_min, L1, Nx);
X2  = linspace(L2, x_max, Nx);
%% 
% Compute the Fourier transform of the incoming soliton on a time grid of 
% $Nt$ equidistant sample points.

S = fft(soliton(-0.8*TimeScale*c2, linspace(0,TimeScale,2*(Nt/2)-1)))';
S = repmat(S,1,Nx);
%% 
% Construct a traveling wave solution in the deep water region based on 
% the Fourier data in $S$.

soliton = real(ifft(S .* exp(1i*W*X2/c2)));
%% 
% Convert the Fourier modes of the reflected wave in the deep water region 
% to numerical values over a grid in $(x, \omega)$ space. Multiply these values 
% with the Fourier coefficients in $S$ and use the function |ifft| to compute 
% the reflected wave in $(x,t)$ space. Note that the first row of the numeric 
% data $R$ consists of NaN values because proper numerical evaluation of the symbolic 
% data $R$ for $\omega = 0$ is not possible. Define the values in the first row 
% of $R$ as the low frequency limits.

R = double(subs(subs(vpa(subs(R)), w, W), x ,X2));
R(1,:) = double((1-sqrt(depthratio)) / (1+sqrt(depthratio)));
reflectedWave = real(ifft(S .* R .* exp(-1i*W*X2/c2)));
%% 
% Use the same approach for the transmitted wave in the shallow water region.

T = double(subs(subs(vpa(subs(T)),w,W),x,X1));
T(1,:) = double(2/(1+sqrt(depthratio)));
transmittedWave = real(ifft(S .* T .* exp(1i*W*X1/c1)));
%% 
% Also, use this approach for the slope region.

U12 = double(subs(subs(vpa(subs(U(x))),w,W),x,X12));
U12(1,:) = double(2/(1+sqrt(depthratio)));
U12 = real(ifft(S .* U12));
%% Plot the Solution
% For a smoother animation, generate additional sample points using trigonometric 
% interpolation along the columns of the plot data.

soliton = interpft(soliton, 10*Nt);
reflectedWave = interpft(reflectedWave, 10*Nt);
U12 = interpft(U12, 10*Nt);
transmittedWave = interpft(transmittedWave, 10*Nt);
%% 
% Create an animated plot of the solution that shows-up in a separate figure 
% window.

figure('Visible', 'on');
plot([x_min, L1, L2, x_max], [-h1, -h1, -h2, -h2], 'Color', 'black')
axis([x_min, x_max, -H-0.1, 0.8])
hold on

line1 = plot(X1,transmittedWave(1,:), 'Color', [0 0 0.62]);
line1.LineWidth = 2;
line12 = plot(X12,U12(1,:), 'Color', [0 0 0.62]);
line12.LineWidth = 2;
line2 = plot(X2,soliton(1,:) + reflectedWave(1,:), 'Color', [0 0 0.62]);
line2.LineWidth = 2;

for t = 2 : size(soliton, 1)*0.35
  line1.YData = transmittedWave(t,:);
  line12.YData = U12(t,:);
  line2.YData = soliton(t,:) + reflectedWave(t,:);
  pause(0.1)
  if mod(t,50) == 0
      savefig(['plot025_', num2str(t)])
  end
end
