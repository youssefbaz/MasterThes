#include <iostream>
#include <assert.h>

//pcl
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>

//octomap 
#include <octomap/octomap.h>
using namespace std;

int main( int argc, char** argv )
{
    if (argc != 3)
    {
        cout<<"Usage: pcd2octomap <input_file> <output_file>"<<endl;
        return -1;
    }

    string input_file = argv[1], output_file = argv[2];
    pcl::PointCloud<pcl::PointXYZRGBA> cloud;
    pcl::io::loadPCDFile<pcl::PointXYZRGBA> ( input_file, cloud );

    cout<<"point cloud loaded, piont size = "<<cloud.points.size()<<endl;

   
    cout<<"copy data into octomap..."<<endl;
    // create an octree object with resolution of 0.5
    octomap::OcTree tree( 0.05 );

    for (auto p:cloud.points)
    {
        
        tree.updateNode( octomap::point3d(p.x, p.y, p.z), true );
    }

    
    tree.updateInnerOccupancy();
    
    tree.writeBinary( output_file );
    cout<<"done."<<endl;

    return 0;
}
