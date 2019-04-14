function pointValue = metricAnalysis(tilesBurned)
% Counts the number of tiles that burned on the outermost edges to give a
% 'point' value to that fire.
% The smaller the better

    hor_edges = [tilesBurned(1,:), tilesBurned(end,:)];
    vert_edges = [tilesBurned(:,1); tilesBurned(:,end)];
    
    all_edges = [hor_edges, vert_edges'];
    
    num_of_pos = length(all_edges);
    burned_edges = sum(all_edges);
    
    pointValue = burned_edges/num_of_pos;
end