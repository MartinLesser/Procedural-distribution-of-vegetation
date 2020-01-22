#include <fstream>
#include <iostream>
#include <time.h>
#include <vector>

#define MAXROWS 8000
#define MAXCOLS 8000
int x_max = MAXROWS, y_max = MAXCOLS;
double matrix[MAXROWS][MAXCOLS];

double line(int x0, int y0, int x1, int y1)
{
    int dx = abs(x1 - x0), sx = x0 < x1 ? 1 : -1;
    int dy = -abs(y1 - y0), sy = y0 < y1 ? 1 : -1;
    int err = dx + dy, e2; /* error value e_xy */
    double sum = 0;

    while (1) {
        if (x0 == x1 && y0 == y1) return sum;
        else sum += matrix[x0][y0];
        e2 = 2 * err;
        if (e2 > dy) { err += dy; x0 += sx; } /* e_xy+e_x > 0 */
        if (e2 < dx) { err += dx; y0 += sy; } /* e_xy+e_y < 0 */
    }
}

struct my_tupel
{
    my_tupel(int _x, int _y)
    {
        x = _x; y = _y;
    }

    int x, y;
};

my_tupel calc_target(int x, int y)
{
    if (x < x_max / 2 && y < y_max / 2) 
    {
        return my_tupel(x_max, y_max);
    }
    else if (x >= x_max / 2 && y < y_max / 2)
    {
        return my_tupel(0, y_max);
    }
    else if (x < x_max / 2 && y >= y_max / 2)
    {
        return my_tupel(x_max, 0);
    }
    else return my_tupel(0, 0);
}

double fRand(double fMin, double fMax)
{
    double f = (double)rand() / RAND_MAX;
    return fMin + f * (fMax - fMin);
}

void randomize_matrix() {
    
    for (int i = 0; i < x_max; i++) {
        for (int j = 0; j < y_max; j++) {
            matrix[i][j] = fRand(0, 1);
        }
    }
}

void print_matrix() 
{ 
    int i, j;
    for (i = 0; i < MAXROWS; i++) {
        for (j = 0; j < MAXCOLS; j++) {
            std::cout << matrix[i][j] << "  ";
        }
        printf("\n");
    }
}

int main()
{
    randomize_matrix();
    //print_matrix();
    std::vector<double> array;
    double time1 = 0.0, tstart;
    tstart = clock();
    for (int x = 0; x < MAXROWS; x++) {
        for (int y = 0; y < MAXCOLS; y++) {
            my_tupel target = calc_target(x, y);
            double sum = line(x, y, target.x, target.y);
            array.push_back(sum);
        }
    }
    time1 += clock() - tstart;
    time1 = time1 / CLOCKS_PER_SEC;
    std::cout << "  time = " << time1 << " sec." << std::endl;

    std::ofstream myfile;
    myfile.open("example.txt");
    for (auto const& value : array)
    {
        myfile << value << " ";
    }
    myfile.close();
}
