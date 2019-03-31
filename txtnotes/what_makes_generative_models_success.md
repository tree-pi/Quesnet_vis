What makes a generative model work?
	_specify_ Inference problem (how to find the latent variable/hypothesis): how to sample for the marginalization?
		_challenge_ The sample can be biased in one clump. 
			_solution_ langevanian random sampling: gradient descent + random walks. To limit: stationary solution as p(x).
				_challenge_ Multimodal landscape, if the peaks is sharp then hard to climb to other peaks.
					_solution_ annealing tricks (simulated tempering).
						_follow-up_ how to theoretically assure this tricks will work?
							_answer_ prove the procedure...(ok i don't understand)
Are GANs successful in learning the distribution? [I understood nothing...]
	_specify_ what are the failures?
		_answer_ just memorizing examples, or mode collapse (some regions not learned).
			_follow-up_ how to test if this failure happened?
Why are word embeddings good?
	_answer_ Arora-Li-Liang-Ma-Risteski 18'