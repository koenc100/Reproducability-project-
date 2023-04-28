# Reproducability-project 
CS4240 Deep Learning (2022/23 Q3) Reproducability project code:

Needed Libraries: 
- OS (3.11.2)
- Numpy (1.11.2)
- PIL (.)
- random 

To make use of the new datasets follow the next steps:

- open the 'picture_gen.py' file.
- make sure 'picture_gen.py' is in the main project folder 
- run the fuctions related to the desired datasets and their respective arguments
  * for circles: Run `generate_circles(arg)`
  * for triangles: Run `generate_triangles(arg)`
  * for perlin noise: Run `perlin_noise(arg)`
- This should generate png files in `/data/SAIL/motion_planning_datasets/ `
- From this folder copy the name of the newly generated dataset in dataloader.py in the function `sail_to_graphs` make sure the regimes are set to:
`regimes = ['train', 'validation', 'test']`
- In data_loader.py at the bottom, change the function call to be as follows:
```
	if _name_ == "_main_":
    		sail_to_graphs('./data/SAIL/motion_planning_datasets/', '<YOUR COPIED DATASET NAME>')
```
-please check in train.py if the dataloader is defined in the function `train_graph_agent()` as follows:
	`dataloaders = loader.get_cmu_data_loaders(args)…`
  
To run the code, 
- open the 
- change the 'path' variable in the 'create_repository' function.
- change parameters in 'if __name__ == __main__' loop. 
- run the code and find your newly created directories on the specified location.
