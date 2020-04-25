clear all
datain=input('input:[xgrip, ygrip, zgrip, theta_yaw]\n'); %in meter and degree

xgrip = datain(1) + 0.150;
ygrip = datain(2) - 0.150;
zgrip = datain(3) - 0.010;
yaw = datain(4)/180*pi;


L1 = 0.152;
L2 = 0.120;
L3 = 0.244;
L4 = 0.093;
L5 = 0.213;
L6 = 0.083;
L7 = 0.083;
L8 = 0.082;
L9 = 0.0535;
L10 = 0.059;


xcen = xgrip - L9*sin(yaw);
ycen = ygrip - L9*cos(yaw);
zcen = zgrip;
theta1 = atan2(ycen, xcen) - asin((L2-L4+L6) / ((xcen^2 + ycen^2)^0.5 ))

theta6 = pi/2 - yaw + theta1

theta5 = -pi/2

X3end = xcen - L7*cos(theta1) + (L6 + 0.027)*cos(pi/2-theta1);

Y3end = ycen - ((L6 + 0.027)*sin(pi/2-theta1) + L7*sin(theta1)); 

Z3end = zcen + L8 + L10;

R = ((X3end)^2 + (Y3end)^2 + (Z3end - L1)^2)^(1/2)
cosa = (R^2 + L3^2 - L5^2)/(2*L3*R);
alpha = acos(cosa);

si = atan2((Z3end-L1),(X3end^2 + Y3end^2)^(1/2));

theta2 = - (alpha + si)

phi = acos((L3^2 + L5^2 - R^2)/(2*L3*L5));

theta3 = pi-phi

theta4 = -(theta3+theta2)

thetas = [rad2deg(theta1) rad2deg(theta2) rad2deg(theta3) rad2deg(theta4) rad2deg(theta5) rad2deg(theta6)]