import { TestBed, inject } from '@angular/core/testing';

import { PossibleBuysService } from './PossibleBuysService';

describe('PossibleBuysService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [PossibleBuysService]
    });
  });

  it('should be created', inject([PossibleBuysService], (service: PossibleBuysService) => {
    expect(service).toBeTruthy();
  }));
});
