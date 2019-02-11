% Renders out the last dataset

Datasets = dir('Datasets/*.h5');
last_dataset = Datasets(end);
last_dataset = fullfile( last_dataset.folder, last_dataset.name);

bio_history = h5read(last_dataset, '/world_data/BiomassAmount');

implay(mat2gray(bio_history), 60);