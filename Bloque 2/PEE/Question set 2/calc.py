p_0_ba = 0.054
p_0_ccca = 0.005557
p_0_t1 = 0.000441
p_0_t2 = 0.002646
p_0_t3 = 0.00247
p_0_cbaa = 0.051786
p_0_cbaa_t1 = 0.04536
p_0_cbaa_t2 = 0.003402
p_0_cbaa_t3 = 0.003024


def calc_new_weights(n_x_y_c1, n_x_y_t1, n_x_y_t2, n_x_y_t3,    n_x_c1, n_x_t1, n_x_t2, n_x_t3,     n_x_y_cabba_t1, n_x_y_cabba_t2, n_x_y_cabba_t3, n_x_cabba_t1, n_x_cabba_t2, n_x_cabba_t3):
    num = 1/p_0_ba * n_x_y_c1 * p_0_ba + (1/p_0_ccca * (n_x_y_t1 * p_0_t1 + n_x_y_t2 * p_0_t2 + n_x_y_t3 * p_0_t3)) + (1/p_0_cbaa * (n_x_y_cabba_t1 * p_0_cbaa_t1 + n_x_y_cabba_t2 * p_0_cbaa_t2 + n_x_y_cabba_t3 * p_0_cbaa_t3))
    den = 1/p_0_ba * n_x_c1 * p_0_ba + (1/p_0_ccca * (n_x_t1 * p_0_t1 + n_x_t2 * p_0_t2 + n_x_t3 * p_0_t3)) + (1/p_0_cbaa * (n_x_cabba_t1 * p_0_cbaa_t1 + n_x_cabba_t2 * p_0_cbaa_t2+ n_x_cabba_t3 * p_0_cbaa_t3))
    return num/den

print('P_0(3|1) = {}'.format(calc_new_weights(1,1, 0,1,  1,2, 2,3,  0,0,1, 2,1,2)))
print('P_0(2|1) = {}'.format(calc_new_weights(0,1, 1,0,  1,2, 2,3,  1,1,0, 2,1,2)))
print('P_0(1|1) = {}'.format(calc_new_weights(0,0, 1,2,  1,2, 2,3,  1,0,1, 2,1,2)))
print('P_0(3|2) = {}'.format(calc_new_weights(0,0, 1,0,  0,1, 1,0,  1,1,0, 1,1,0)))
print('P_0(1|2) = {}'.format(calc_new_weights(0,1, 0,0,  0,1, 1,0,  0,0,0, 1,1,0)))
print('P_0(3|3) = {}'.format(calc_new_weights(0,0, 0,0,  1,1, 1,1,  0,1,1, 1,2,2)))
print('P_0(#|3) = {}'.format(calc_new_weights(1,1, 1,1,  1,1, 1,1,  1,1,1, 1,2,2)))
print('P_0(a|1) = {}'.format(calc_new_weights(0,0, 0,0,  1,2, 2,3,  0,0,0, 2,1,2)))
print('P_0(b|1) = {}'.format(calc_new_weights(1,0, 0,0,  1,2, 2,3,  1,0,1, 2,1,2)))
print('P_0(c|1) = {}'.format(calc_new_weights(0,2, 2,3,  1,2, 2,3,  1,1,1, 2,1,2)))
print('P_0(a|2) = {}'.format(calc_new_weights(0,0, 0,0,  0,1, 1,0,  1,0,0, 1,1,0)))
print('P_0(b|2) = {}'.format(calc_new_weights(0,0, 0,0,  0,1, 1,0,  0,1,0, 1,1,0)))
print('P_0(c|2) = {}'.format(calc_new_weights(0,1, 1,0,  0,1, 1,0,  0,0,0, 1,1,0)))
print('P_0(a|3) = {}'.format(calc_new_weights(1,1, 1,1,  1,1, 1,1,  1,2,2, 1,2,2)))
print('P_0(b|3) = {}'.format(calc_new_weights(0,0, 0,0,  1,1, 1,1,  0,0,0, 1,2,2)))
print('P_0(c|3) = {}'.format(calc_new_weights(0,0, 0,0,  1,1, 1,1,  0,0,0, 1,2,2)))